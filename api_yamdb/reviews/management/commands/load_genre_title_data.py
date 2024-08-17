from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Genre, GenreTitle, Title


class Command(BaseCommand):

    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            print('GenreTitle data already loaded!')
            return
        print('Loading GenreTitle data...')

        with open('static/data/genre_title.csv', newline='',
                  encoding='utf8') as genre_title_csv:
            reader = DictReader(genre_title_csv, delimiter=',')
            for row in reader:
                genre = Genre.objects.get(pk=row['genre_id'])
                title = Title.objects.get(pk=row['title_id'])
                genre_title = GenreTitle(
                    id=row['id'], genre=genre, title=title)
                genre_title.save()
