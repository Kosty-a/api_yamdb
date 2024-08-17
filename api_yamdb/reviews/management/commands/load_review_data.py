from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from reviews.models import Review, Title

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Review.objects.exists():
            print('Review data already loaded!')
            return
        print('Loading review data...')

        with open('static/data/review.csv', newline='',
                  encoding='utf8') as review_csv:
            reader = DictReader(review_csv, delimiter=',')
            for row in reader:
                title = Title.objects.get(pk=row['title_id'])
                author = User.objects.get(pk=row['author'])
                review = Review(
                    id=row['id'], title=title, text=row['text'], author=author,
                    score=row['score'], pub_date=row['pub_date'])
                review.save()
