from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Title


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Title.objects.exists():
            self.stderr.write('Title data already loaded!')
            return

        self.stdout.write('Loading Title data...')

        with open(settings.STATIC_DATA_URL + 'titles.csv', newline='',
                  encoding='utf8') as title_csv:
            reader = DictReader(title_csv, delimiter=',')
            for row in reader:
                category = Category.objects.get(pk=row['category'])
                title = Title(
                    id=row['id'], name=row['name'],
                    year=row['year'], category=category)
                title.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded!'))
