from django.core.exceptions import ValidationError

from core.constants import ME


def validate_not_me(value):
    if value == ME:
        raise ValidationError('Invalid username')
