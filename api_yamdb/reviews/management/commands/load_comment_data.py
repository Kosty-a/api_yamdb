from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from reviews.models import Comment, Review

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Comment.objects.exists():
            print('Comment data already loaded!')
            return
        print('Loading comment data...')

        with open('static/data/comments.csv', newline='',
                  encoding='utf8') as comment_csv:
            reader = DictReader(comment_csv, delimiter=',')
            for row in reader:
                review = Review.objects.get(pk=row['review_id'])
                author = User.objects.get(pk=row['author'])
                comment = Comment(
                    id=row['id'], review=review, text=row['text'],
                    author=author, pub_date=row['pub_date'])
                comment.save()
