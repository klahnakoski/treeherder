from jx_base.expressions import NULL
from jx_mysql.mysql import MySQL
from jx_mysql.mysql_snowflake_extractor import MySqlSnowflakeExtractor
from mo_future import text
from mo_json import value2json
from mo_logs.strings import strip
from mo_sql import SQL
from mo_testing.fuzzytestcase import assertAlmostEqual
from pyLibrary.convert import table2tab


def test_make_repository(test_repository, extract_job_settings):
    # TEST EXISTING FIXTURE MAKES AN OBJECT IN THE DATABASE
    source = MySQL(extract_job_settings.source.database)
    with source.transaction():
        result = source.query(SQL("SELECT * from repository"))

    # verify the repository object is the one we expect
    assert result[0].id == test_repository.id
    assert result[0].tc_root_url == test_repository.tc_root_url


def test_make_failure_class(failure_class, extract_job_settings):
    # TEST I CAN MAKE AN OBJECT IN THE DATABASE
    source = MySQL(extract_job_settings.source.database)
    with source.transaction():
        result = source.query(SQL("SELECT * from failure_classification"))

    # verify the repository object is the one we expect
    assert result[0].name == "not classified"


def test_make_job(complex_job, extract_job_settings):
    source = MySQL(extract_job_settings.source.database)
    with source.transaction():
        result = source.query(SQL("SELECT count(1) as num from job_detail"))

    assert result[0].num == 4


def test_extract_job(complex_job, extract_job_settings, now):
    source = MySQL(extract_job_settings.source.database)
    # with source.transaction():
    #     result = source.query(SQL("SELECT * from text_log_error"))
    # assert result[0].guid == complex_job.guid
    extractor = MySqlSnowflakeExtractor(extract_job_settings.source)
    sql = extractor.get_sql(SQL("SELECT " + text(complex_job.id) + " as id"))



    acc = []
    with source.transaction():
        cursor = list(source.query(sql, stream=True, row_tuples=True))
        tab = table2tab([c.column_alias for c in extractor.columns], cursor)
        extractor.construct_docs(cursor, acc.append, False)
    example = value2json(acc, pretty=True)

    doc = acc[0]
    doc.guid = complex_job.guid
    doc.last_modified = complex_job.last_modified

    assertAlmostEqual(acc, JOB, places=4)


# VERIFY SQL OVER DATABASE
def test_extract_job_sql(extract_job_settings, transactional_db):
    extractor = MySqlSnowflakeExtractor(extract_job_settings.source)
    sql = extractor.get_sql(SQL("SELECT 0"))
    assert strip(sql.sql) == strip(EXTRACT_JOB_SQL)


EXTRACT_JOB_SQL = """
SELECT
 * 
FROM
(
SELECT
 `t1`.`id` AS `c0`, `t1`.`guid` AS `c1`, `t1`.`coalesced_to_guid` AS `c2`, `t1`.`who` AS `c3`, `t1`.`reason` AS `c4`, `t1`.`result` AS `c5`, `t1`.`state` AS `c6`, `t1`.`submit_time` AS `c7`, `t1`.`start_time` AS `c8`, `t1`.`end_time` AS `c9`, `t1`.`last_modified` AS `c10`, `t1`.`running_eta` AS `c11`, `t1`.`tier` AS `c12`, `t2`.`id` AS `c13`, `t2`.`name` AS `c14`, `t3`.`id` AS `c15`, `t3`.`os_name` AS `c16`, `t3`.`platform` AS `c17`, `t3`.`architecture` AS `c18`, `t4`.`id` AS `c19`, `t4`.`name` AS `c20`, `t5`.`id` AS `c21`, `t5`.`symbol` AS `c22`, `t5`.`name` AS `c23`, `t5`.`description` AS `c24`, `t6`.`id` AS `c25`, `t6`.`symbol` AS `c26`, `t6`.`name` AS `c27`, `t6`.`description` AS `c28`, `t7`.`id` AS `c29`, `t7`.`name` AS `c30`, `t8`.`id` AS `c31`, `t8`.`os_name` AS `c32`, `t8`.`platform` AS `c33`, `t8`.`architecture` AS `c34`, `t9`.`id` AS `c35`, `t9`.`option_collection_hash` AS `c36`, `t10`.`id` AS `c37`, `t10`.`name` AS `c38`, `t11`.`id` AS `c39`, `t11`.`revision` AS `c40`, `t11`.`author` AS `c41`, `t11`.`time` AS `c42`, `t12`.`id` AS `c43`, `t12`.`name` AS `c44`, `t13`.`id` AS `c45`, `t13`.`name` AS `c46`, `t13`.`signature` AS `c47`, `t13`.`build_os_name` AS `c48`, `t13`.`build_platform` AS `c49`, `t13`.`build_architecture` AS `c50`, `t13`.`machine_os_name` AS `c51`, `t13`.`machine_platform` AS `c52`, `t13`.`machine_architecture` AS `c53`, `t13`.`job_group_name` AS `c54`, `t13`.`job_group_symbol` AS `c55`, `t13`.`job_type_name` AS `c56`, `t13`.`job_type_symbol` AS `c57`, `t13`.`option_collection_hash` AS `c58`, `t13`.`build_system_type` AS `c59`, `t13`.`repository` AS `c60`, `t13`.`first_submission_timestamp` AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`,  NULL  AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`, `t14`.`id` AS `c94`, `t14`.`name` AS `c95`, `t15`.`id` AS `c96`, `t15`.`name` AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
LEFT JOIN
`treeherder`.`failure_classification` AS `t2` ON `t2`.`id` = `t1`.`autoclassify_status`
LEFT JOIN
`treeherder`.`build_platform` AS `t3` ON `t3`.`id` = `t1`.`build_platform_id`
LEFT JOIN
`treeherder`.`failure_classification` AS `t4` ON `t4`.`id` = `t1`.`failure_classification_id`
LEFT JOIN
`treeherder`.`job_group` AS `t5` ON `t5`.`id` = `t1`.`job_group_id`
LEFT JOIN
`treeherder`.`job_type` AS `t6` ON `t6`.`id` = `t1`.`job_type_id`
LEFT JOIN
`treeherder`.`machine` AS `t7` ON `t7`.`id` = `t1`.`machine_id`
LEFT JOIN
`treeherder`.`machine_platform` AS `t8` ON `t8`.`id` = `t1`.`machine_platform_id`
LEFT JOIN
`treeherder`.`option_collection` AS `t9` ON `t9`.`option_collection_hash` = `t1`.`option_collection_hash`
LEFT JOIN
`treeherder`.`product` AS `t10` ON `t10`.`id` = `t1`.`product_id`
LEFT JOIN
`treeherder`.`push` AS `t11` ON `t11`.`id` = `t1`.`push_id`
LEFT JOIN
`treeherder`.`repository` AS `t12` ON `t12`.`id` = `t1`.`repository_id`
LEFT JOIN
`treeherder`.`reference_data_signatures` AS `t13` ON `t13`.`id` = `t1`.`signature_id`
LEFT JOIN
`treeherder`.`option` AS `t14` ON `t14`.`id` = `t9`.`option_id`
LEFT JOIN
`treeherder`.`repository` AS `t15` ON `t15`.`id` = `t11`.`repository_id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`, `t2`.`id` AS `c62`, `t2`.`bug_id` AS `c63`, `t2`.`created` AS `c64`, `t2`.`job_id` AS `c65`, `t2`.`user_id` AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`,  NULL  AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`bug_job_map` AS `t2` ON `t2`.`job_id` = `t1`.`id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`, `t2`.`id` AS `c67`, `t2`.`title` AS `c68`, `t2`.`value` AS `c69`, `t2`.`url` AS `c70`, `t2`.`job_id` AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`,  NULL  AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`job_detail` AS `t2` ON `t2`.`job_id` = `t1`.`id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`, `t2`.`id` AS `c72`, `t2`.`name` AS `c73`, `t2`.`url` AS `c74`, `t2`.`status` AS `c75`, `t2`.`job_id` AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`,  NULL  AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`job_log` AS `t2` ON `t2`.`job_id` = `t1`.`id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`, `t2`.`id` AS `c77`, `t2`.`text` AS `c78`, `t2`.`created` AS `c79`, `t2`.`failure_classification_id` AS `c80`, `t2`.`job_id` AS `c81`, `t2`.`user_id` AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`,  NULL  AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`, `t3`.`id` AS `c118`, `t3`.`name` AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`job_note` AS `t2` ON `t2`.`job_id` = `t1`.`id`
LEFT JOIN
`treeherder`.`failure_classification` AS `t3` ON `t3`.`id` = `t2`.`failure_classification_id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`, `t2`.`job_id` AS `c83`, `t2`.`task_id` AS `c84`, `t2`.`retry_id` AS `c85`,  NULL  AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`taskcluster_metadata` AS `t2` ON `t2`.`job_id` = `t1`.`id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`, `t2`.`id` AS `c86`, `t2`.`name` AS `c87`, `t2`.`started` AS `c88`, `t2`.`finished` AS `c89`, `t2`.`started_line_number` AS `c90`, `t2`.`finished_line_number` AS `c91`, `t2`.`result` AS `c92`, `t2`.`job_id` AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`text_log_step` AS `t2` ON `t2`.`job_id` = `t1`.`id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`, `t2`.`id` AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`,  NULL  AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`, `t3`.`id` AS `c98`, `t3`.`job_guid` AS `c99`, `t3`.`action` AS `c100`, `t3`.`line` AS `c101`, `t3`.`test` AS `c102`, `t3`.`subtest` AS `c103`, `t3`.`status` AS `c104`, `t3`.`expected` AS `c105`, `t3`.`message` AS `c106`, `t3`.`signature` AS `c107`, `t3`.`level` AS `c108`, `t3`.`stack` AS `c109`, `t3`.`best_is_verified` AS `c112`, `t3`.`created` AS `c113`, `t3`.`modified` AS `c114`, `t3`.`best_classification_id` AS `c115`, `t3`.`job_log_id` AS `c116`, `t3`.`repository_id` AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`,  NULL  AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`, `t4`.`id` AS `c124`, `t4`.`bug_number` AS `c125`, `t4`.`created` AS `c126`, `t4`.`modified` AS `c127`, `t5`.`id` AS `c128`, `t5`.`name` AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`job_log` AS `t2` ON `t2`.`job_id` = `t1`.`id`
JOIN
`treeherder`.`failure_line` AS `t3` ON `t3`.`job_log_id` = `t2`.`id`
LEFT JOIN
`treeherder`.`classified_failure` AS `t4` ON `t4`.`id` = `t3`.`best_classification_id`
LEFT JOIN
`treeherder`.`repository` AS `t5` ON `t5`.`id` = `t3`.`repository_id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`, `t2`.`id` AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`, `t3`.`id` AS `c120`, `t3`.`line` AS `c121`, `t3`.`line_number` AS `c122`, `t3`.`step_id` AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`,  NULL  AS `c130`,  NULL  AS `c131`,  NULL  AS `c132`,  NULL  AS `c133`,  NULL  AS `c134`,  NULL  AS `c135`,  NULL  AS `c136`,  NULL  AS `c137`,  NULL  AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`text_log_step` AS `t2` ON `t2`.`job_id` = `t1`.`id`
JOIN
`treeherder`.`text_log_error` AS `t3` ON `t3`.`step_id` = `t2`.`id`
UNION ALL

SELECT
 `t1`.`id` AS `c0`,  NULL  AS `c1`,  NULL  AS `c2`,  NULL  AS `c3`,  NULL  AS `c4`,  NULL  AS `c5`,  NULL  AS `c6`,  NULL  AS `c7`,  NULL  AS `c8`,  NULL  AS `c9`,  NULL  AS `c10`,  NULL  AS `c11`,  NULL  AS `c12`,  NULL  AS `c13`,  NULL  AS `c14`,  NULL  AS `c15`,  NULL  AS `c16`,  NULL  AS `c17`,  NULL  AS `c18`,  NULL  AS `c19`,  NULL  AS `c20`,  NULL  AS `c21`,  NULL  AS `c22`,  NULL  AS `c23`,  NULL  AS `c24`,  NULL  AS `c25`,  NULL  AS `c26`,  NULL  AS `c27`,  NULL  AS `c28`,  NULL  AS `c29`,  NULL  AS `c30`,  NULL  AS `c31`,  NULL  AS `c32`,  NULL  AS `c33`,  NULL  AS `c34`,  NULL  AS `c35`,  NULL  AS `c36`,  NULL  AS `c37`,  NULL  AS `c38`,  NULL  AS `c39`,  NULL  AS `c40`,  NULL  AS `c41`,  NULL  AS `c42`,  NULL  AS `c43`,  NULL  AS `c44`,  NULL  AS `c45`,  NULL  AS `c46`,  NULL  AS `c47`,  NULL  AS `c48`,  NULL  AS `c49`,  NULL  AS `c50`,  NULL  AS `c51`,  NULL  AS `c52`,  NULL  AS `c53`,  NULL  AS `c54`,  NULL  AS `c55`,  NULL  AS `c56`,  NULL  AS `c57`,  NULL  AS `c58`,  NULL  AS `c59`,  NULL  AS `c60`,  NULL  AS `c61`,  NULL  AS `c62`,  NULL  AS `c63`,  NULL  AS `c64`,  NULL  AS `c65`,  NULL  AS `c66`,  NULL  AS `c67`,  NULL  AS `c68`,  NULL  AS `c69`,  NULL  AS `c70`,  NULL  AS `c71`,  NULL  AS `c72`,  NULL  AS `c73`,  NULL  AS `c74`,  NULL  AS `c75`,  NULL  AS `c76`,  NULL  AS `c77`,  NULL  AS `c78`,  NULL  AS `c79`,  NULL  AS `c80`,  NULL  AS `c81`,  NULL  AS `c82`,  NULL  AS `c83`,  NULL  AS `c84`,  NULL  AS `c85`, `t2`.`id` AS `c86`,  NULL  AS `c87`,  NULL  AS `c88`,  NULL  AS `c89`,  NULL  AS `c90`,  NULL  AS `c91`,  NULL  AS `c92`,  NULL  AS `c93`,  NULL  AS `c94`,  NULL  AS `c95`,  NULL  AS `c96`,  NULL  AS `c97`,  NULL  AS `c98`,  NULL  AS `c99`,  NULL  AS `c100`,  NULL  AS `c101`,  NULL  AS `c102`,  NULL  AS `c103`,  NULL  AS `c104`,  NULL  AS `c105`,  NULL  AS `c106`,  NULL  AS `c107`,  NULL  AS `c108`,  NULL  AS `c109`,  NULL  AS `c112`,  NULL  AS `c113`,  NULL  AS `c114`,  NULL  AS `c115`,  NULL  AS `c116`,  NULL  AS `c117`,  NULL  AS `c118`,  NULL  AS `c119`, `t3`.`id` AS `c120`,  NULL  AS `c121`,  NULL  AS `c122`,  NULL  AS `c123`,  NULL  AS `c124`,  NULL  AS `c125`,  NULL  AS `c126`,  NULL  AS `c127`,  NULL  AS `c128`,  NULL  AS `c129`, `t4`.`id` AS `c130`, `t4`.`score` AS `c131`, `t4`.`classified_failure_id` AS `c132`, `t4`.`text_log_error_id` AS `c133`, `t4`.`matcher_name` AS `c134`, `t5`.`id` AS `c135`, `t5`.`bug_number` AS `c136`, `t5`.`created` AS `c137`, `t5`.`modified` AS `c138` 
FROM
(SELECT 0) AS `t0`
LEFT JOIN
`treeherder`.`job` AS `t1` ON `t1`.`id` = `t0`.`id`
JOIN
`treeherder`.`text_log_step` AS `t2` ON `t2`.`job_id` = `t1`.`id`
JOIN
`treeherder`.`text_log_error` AS `t3` ON `t3`.`step_id` = `t2`.`id`
JOIN
`treeherder`.`text_log_error_match` AS `t4` ON `t4`.`text_log_error_id` = `t3`.`id`
LEFT JOIN
`treeherder`.`classified_failure` AS `t5` ON `t5`.`id` = `t4`.`classified_failure_id`) AS `a`
ORDER BY
 `c0` IS NOT NULL , `c0`, `c62` IS NOT NULL , `c62`, `c67` IS NOT NULL , `c67`, `c72` IS NOT NULL , `c72`, `c77` IS NOT NULL , `c77`, `c83` IS NOT NULL , `c83`, `c86` IS NOT NULL , `c86`, `c98` IS NOT NULL , `c98`, `c120` IS NOT NULL , `c120`, `c130` IS NOT NULL , `c130`
"""


JOB = [
    {
        "autoclassify_status": 1,
        "build_platform": {
            "architecture": "x86",
            "os_name": "my_os",
            "platform": "my_platform",
        },
        "submit_time": 1578427253,
        "start_time": 1578430841,
        "end_time": 1578432680,
        "failure_classification": "not classified",
        "id": 1,
        "job_detail": [
            {
                "title": "artifact uploaded",
                "url": "https://example.com/api/queue/v1/task/WWb9ExAvQUa78ku0DIxdSQ/runs/0/artifacts/public/test_info/wpt_raw.log",
                "value": "wpt_raw.log",
            },
            {
                "title": "artifact uploaded",
                "url": "https://example.com/api/queue/v1/task/WWb9ExAvQUa78ku0DIxdSQ/runs/0/artifacts/public/test_info/wptreport.json",
                "value": "wptreport.json",
            },
            {"title": "CPU usage", "value": "26.8%"},
            {"title": "I/O read bytes / time", "value": "179,900,416 / 41"},
        ],
        "job_group": {"description": NULL, "name": "myjobgroup", "symbol": "S"},
        "job_log": [
            {
                "name": "builds-4h",
                "status": 1,
                "url": "https://example.com/api/queue/v1/task/WWb9ExAvQUa78ku0DIxdSQ/runs/0/artifacts/public/logs/live_backing.log",
            },
            {
                "failure_line": [
                    {
                        "action": "test_groups",
                        "best_classification": {
                            "bug_number": 1579215297,
                            "created": 2,
                            "modified": "autoland",
                        },
                        "best_is_verified": 1579215297,
                        "created": 1,
                        "line": 15,
                        "line_number": 1,
                        "modified": 2,
                    },
                    {
                        "action": "crash",
                        "best_classification": {
                            "bug_number": 1579215447,
                            "created": 2,
                            "modified": "autoland",
                        },
                        "best_is_verified": 1579215447,
                        "created": 1,
                        "line": 24031,
                        "line_number": 1,
                        "modified": 2,
                        "signature": "@ mozilla::dom::CustomElementData::SetCustomElementDefinition(mozilla::dom::CustomElementDefinition*)",
                        "test": "/custom-elements/upgrading.html",
                    },
                ],
                "name": "errorsummary_json",
                "status": 1,
                "url": "https://example.com/api/queue/v1/task/WWb9ExAvQUa78ku0DIxdSQ/runs/0/artifacts/public/test_info/wpt_errorsummary.log",
            },
        ],
        "job_type": {"name": "myjob", "symbol": "j"},
        "machine": {"name": "mymachine"},
        "machine_platform": {
            "architecture": "x86",
            "os_name": "my_os",
            "platform": "my_platform",
        },
        "options": {"option": "debug"},
        "product": {"name": "myproduct"},
        "push": {
            "author": "testing@mozilla.com",
            "repository": "autoland",
            "revision": "ae6bb3a1066959a8c43d003a3caab0af769455bf",
            "time": 1578445105,
        },
        "reason": "scheduled",
        "repository": "test_treeherder_jobs",
        "result": "success",
        "signature": {
            "build_architecture": "x86",
            "build_os_name": "my_os",
            "build_platform": "my_platform",
            "build_system_type": "buildbot",
            "first_submission_timestamp": 0,
            "job_group_name": "myjobgroup",
            "job_group_symbol": "S",
            "job_type_name": "myjob",
            "job_type_symbol": "j",
            "machine_architecture": "x86",
            "machine_os_name": "my_os",
            "machine_platform": "my_platform",
            "name": "myreferencedatasignaeture",
            "option_collection_hash": "my_option_hash",
            "repository": "test_treeherder_jobs",
            "signature": "1234",
        },
        "state": "completed",
        "taskcluster_metadata": [{"retry_id": 0, "task_id": "WWb9ExAvQUa78ku0DIxdSQ"}],
        "text_log_step": [
            {
                "finished_line_number": 88739,
                "name": "Unnamed step",
                "result": 7,
                "started_line_number": 0,
                "text_log_error": [
                    {"line": "line contents here", "line_number": 619845839},
                    {"line": "ERROR! more line contents", "line_number": 6},
                ],
            }
        ],
        "tier": 1,
        "who": "example@mozilla.com",
    }
]
