from core.constants import ME
from django.core.exceptions import ValidationError


def validate_not_me(value):
    if value == ME:
        raise ValidationError('Invalid username')
