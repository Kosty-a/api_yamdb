from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Genre, GenreTitle, Title


class Command(BaseCommand):

    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            self.stderr.write('GenreTitle data already loaded!')
            return

        self.stdout.write('Loading GenreTitle data...')

        with open(settings.STATIC_DATA_URL + 'genre_title.csv', newline='',
                  encoding='utf8') as genre_title_csv:
            reader = DictReader(genre_title_csv, delimiter=',')
            for row in reader:
                genre = Genre.objects.get(pk=row['genre_id'])
                title = Title.objects.get(pk=row['title_id'])
                genre_title = GenreTitle(
                    id=row['id'], genre=genre, title=title)
                genre_title.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded!'))
