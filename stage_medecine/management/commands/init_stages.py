from django.core.management import CommandError, BaseCommand
import csv


class Command(BaseCommand):
    help = 'Import stage data from csv'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--csv', dest='csv', default=None,
            help='Specifies the csv file to fetch',
        )

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        password = options.get('csv')
