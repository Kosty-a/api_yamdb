from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Genre.objects.exists():
            self.stderr.write('Genre data already loaded!')
            return

        self.stdout.write('Loading Genre data...')

        with open(settings.STATIC_DATA_URL + 'genre.csv', newline='',
                  encoding='utf8') as genre_csv:
            reader = DictReader(genre_csv, delimiter=',')
            for row in reader:
                genre = Genre(
                    id=row['id'], name=row['name'], slug=row['slug'])
                genre.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded!'))
