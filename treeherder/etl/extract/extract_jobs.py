from redis import Redis

from jx_bigquery import bigquery
from mo_files import File
from mo_json import json2value
from mo_logs import Log, startup, constants
from mo_times.dates import parse
from mo_sql import (
    SQL,
)
from jx_mysql.mysql import MySQL
from jx_mysql.mysql_snowflake_extractor import MySqlSnowflakeExtractor
from jx_sqlite.sqlite import sql_query
from treeherder.etl.extract import VENDOR_PATH

CONFIG_FILE = (File.new_instance(__file__).parent / "extract_jobs.json").abs_path

_keep_import = VENDOR_PATH


class ExtractJobs:
    def run(self):
        # SETUP LOGGING
        settings = startup.read_settings(filename=CONFIG_FILE)
        constants.set(settings.constants)
        Log.start(settings.debug)

        # RECOVER LAST SQL STATE
        redis = Redis()
        state = redis.get(settings.extractor.key)

        if not state:
            state = (0, 0)
            redis.set(settings.extractor.key, state)
        last_modified, job_id = json2value(state)

        # SCAN SCHEMA, GENERATE EXTRACTION SQL
        extractor = MySqlSnowflakeExtractor(settings.source)
        canonical_sql = extractor.get_sql(SQL("SELECT 0"))

        # ENSURE PREVIOUS RUN DID NOT CHANGE ANYTHING
        old_sql = redis.get(settings.extractor.sql)
        if old_sql and old_sql != canonical_sql:
            Log.error("Schema has changed")
        redis.set(settings.extractor.sql, canonical_sql)

        # SETUP SOURCE
        source = MySQL(settings.source.database)

        # SETUP DESTINATION
        destination = bigquery.Dataset(settings.destination).get_or_create_table(
            settings.destination
        )

        while True:
            Log.note(
                "Extracting jobs for {{last_modified|datetime}}, {{job_id}}",
                last_modified=last_modified,
                job_id=job_id,
            )
            get_ids = sql_query({
                "from": "job",
                "select": ["id"],
                "where": {
                    "or": [
                        {"gt": {"last_modified": parse(last_modified)}},
                        {
                            "and": [
                                {"eq": {"last_modified": parse(last_modified)}},
                                {"gt": {"id": job_id}},
                            ]
                        },
                    ]
                },
                "sort": ["last_modified", "id"],
                "limit": settings.extractor.chunk_size
            })

            sql = extractor.get_sql(get_ids)

            # PULL FROM source, AND PUSH TO destination
            acc = []
            cursor = source.query(sql, stream=True, row_tuples=True)
            extractor.construct_docs(self, cursor, acc.append, False)
            if not acc:
                break
            destination.extend(acc)

            # RECORD THE STATE
            last_doc = acc[-1]
            last_modified, job_id = last_doc.last_modified, last_doc.id
            redis.set(settings.extractor.key, last_modified, job_id)

        Log.note("done job extraction")
