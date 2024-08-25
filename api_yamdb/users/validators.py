from django.core.exceptions import ValidationError

from core.constants import INVALID_USERNAME_ME


def validate_not_me(value):
    if value == INVALID_USERNAME_ME:
        raise ValidationError('Invalid username')
