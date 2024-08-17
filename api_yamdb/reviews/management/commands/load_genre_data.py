from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Genre.objects.exists():
            print('Genre data already loaded!')
            return
        print('Loading genre data...')

        with open('static/data/genre.csv', newline='',
                  encoding='utf8') as genre_csv:
            reader = DictReader(genre_csv, delimiter=',')
            for row in reader:
                genre = Genre(
                    id=row['id'], name=row['name'], slug=row['slug'])
                genre.save()
