from api_yamdb.settings import FROM_EMAIL
from core.constants import (CONFIRMATION_CODE_LENGTH, MAX_EMAIL_LENGTH,
                            MAX_USERNAME_LENGTH, REGEX_USERNAME)
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.validators import validate_not_me

from api_users.utils import generate_confirmation_code


User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    '''Сериализатор для создания пользователя.'''
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[RegexValidator(regex=REGEX_USERNAME), validate_not_me])
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)

    def create(self, validated_data):
        user = User.objects.get_or_create(**validated_data)[0]
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            subject='Confirmation code',
            message=confirmation_code,
            from_email=FROM_EMAIL,
            recipient_list=[validated_data['email']]
        )

        return user

    def validate(self, data):
        username = data['username']
        email = data['email']

        try:
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError('Invalid email for user')
        except ObjectDoesNotExist:
            pass

        try:
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError('Invalid username for user')
        except ObjectDoesNotExist:
            pass

        return data


class ObtainTokenSerializer(serializers.Serializer):
    '''Сериализатор для получения токена.'''

    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[RegexValidator(regex=REGEX_USERNAME), validate_not_me])
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH)

    def validate_username(self, value):
        get_object_or_404(User, username=value)
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
