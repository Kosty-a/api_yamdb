from core.constants import (ADMIN, CONFIRMATION_CODE_LENGTH, MAX_EMAIL_LENGTH,
                            MAX_USERNAME_LENGTH, MODERATOR, REGEX_USERNAME,
                            USER)
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_not_me


ROLE_CHOICES = (
    (USER, 'пользователь'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'админ')
)


class CustomUser(AbstractUser):
    '''Модель пользователя.'''

    username = models.CharField(
        'Имя пользователя', max_length=MAX_USERNAME_LENGTH, unique=True,
        validators=[
            RegexValidator(
                regex=REGEX_USERNAME),
            validate_not_me,
        ])
    email = models.EmailField(
        'Почта', max_length=MAX_EMAIL_LENGTH, unique=True)
    bio = models.TextField('Био', blank=True, null=True)
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, default=USER,
        max_length=max([len(role[0]) for role in ROLE_CHOICES]))
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True,
        null=True, max_length=CONFIRMATION_CODE_LENGTH)

    @property
    def is_admin(self):
        return (
            self.is_superuser or self.is_staff or self.role == ADMIN
        )

    @property
    def is_moderator(self):
        return (
            self.role == MODERATOR
        )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
