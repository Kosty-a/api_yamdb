from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Category.objects.exists():
            self.stderr.write('Category data already loaded!')
            return

        self.stdout.write('Loading Category data...')

        with open(settings.STATIC_DATA_URL + 'category.csv', newline='',
                  encoding='utf8') as category_csv:
            reader = DictReader(category_csv, delimiter=',')
            for row in reader:
                category = Category(
                    id=row['id'], name=row['name'], slug=row['slug'])
                category.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded!'))
