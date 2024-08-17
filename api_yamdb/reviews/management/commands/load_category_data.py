from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Category.objects.exists():
            print('Category data already loaded!')
            return
        print('Loading category data...')

        with open('static/data/category.csv', newline='',
                  encoding='utf8') as category_csv:
            reader = DictReader(category_csv, delimiter=',')
            for row in reader:
                category = Category(
                    id=row['id'], name=row['name'], slug=row['slug'])
                category.save()
