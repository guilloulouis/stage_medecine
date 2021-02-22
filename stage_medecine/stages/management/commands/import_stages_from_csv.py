from django.core.management import BaseCommand
import pandas as pd

from stages.models import Category, Stage


class Command(BaseCommand):
    help = 'Import a list of stage in the database'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--csv', dest='csv', default=None,
            help='Specify the csv file to parse',
        )

    def handle(self, *args, **options):
        csv = options.get('csv')
        csv_reader = pd.read_csv(csv)
        stages_to_create = []
        for index, item in csv_reader.iterrows():
            stage_raw = item['Stage']
            split = stage_raw.split('(')
            stage_name = split[0].strip()
            if len(split) > 1:
                category_name = split[1].replace(')', '').strip()
                category_object, created = Category.objects.get_or_create(name=category_name)
            else:
                category_object = None
            stages_to_create.append(Stage(name=stage_name, place_max=item['places'], category=category_object))
        Stage.objects.bulk_create(stages_to_create)
