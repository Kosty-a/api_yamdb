from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


ROLE_CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'админ')
)


class CustomUser(AbstractUser):
    password = None
    groups = None
    user_permissions = None

    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z'),
        ])
    email = models.EmailField('Почта', max_length=254, unique=True)
    first_name = models.CharField(
        'Имя', max_length=150, blank=True, null=True)
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True, null=True)
    bio = models.TextField('Био', blank=True, null=True)
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, default='user', max_length=9)
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True, null=True, max_length=4)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
