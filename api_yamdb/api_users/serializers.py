from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_users.utils import generate_confirmation_code
from core.constants import (CONFIRMATION_CODE_LENGTH, MAX_EMAIL_LENGTH,
                            MAX_USERNAME_LENGTH, REGEX_USERNAME)
from users.validators import validate_not_me


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
            from_email=settings.FROM_EMAIL,
            recipient_list=[validated_data['email']]
        )

        return user

    def validate(self, data):
        username = data['username']
        email = data['email']

        if User.objects.filter(username=username, email=email):
            return data
        elif User.objects.filter(username=username):
            raise serializers.ValidationError('Invalid email for user')
        elif User.objects.filter(email=email):
            raise serializers.ValidationError('Invalid username for user')

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

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']

        user = User.objects.get(username=username)

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Invalid confirmation code')

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
