from django.core.exceptions import ValidationError

from core.constants import INVALID_USERNAME


def validate_not_me(value):
    if value == INVALID_USERNAME:
        raise ValidationError('Invalid username')
