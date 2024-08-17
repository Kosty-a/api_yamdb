from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Title


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Title.objects.exists():
            print('Title data already loaded!')
            return
        print('Loading title data...')

        with open('static/data/titles.csv', newline='',
                  encoding='utf8') as title_csv:
            reader = DictReader(title_csv, delimiter=',')
            for row in reader:
                category = Category.objects.get(pk=row['category'])
                title = Title(
                    id=row['id'], name=row['name'],
                    year=row['year'], category=category)
                title.save()
