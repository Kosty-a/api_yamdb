from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.exists():
            print('User data already loaded!')
            return
        print('Loading user data...')

        with open('static/data/users.csv', newline='',
                  encoding='utf8') as user_csv:
            reader = DictReader(user_csv, delimiter=',')
            for row in reader:
                user = User(
                    id=row['id'], username=row['username'],
                    email=row['email'], role=row['role'], bio=row['bio'],
                    first_name=row['first_name'], last_name=row['last_name'])
                user.save()
