from django.core.management.base import BaseCommand

from treeherder.etl.extract.extract_jobs import ExtractJobs


class Command(BaseCommand):
    """Management command to extract jobs"""
    help = "Extract recently changed jobs from Treeherder, and push them to BigQuery"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action='store_true',
            dest="force",
            help="Ignore changed schema"
        )
        parser.add_argument(
            "--restart",
            action='store_true',
            dest="restart",
            help="start extraction from the beginning"
        )

    def handle(self, *args, **options):
        force = options["force"]
        ExtractJobs().run(force=force)
