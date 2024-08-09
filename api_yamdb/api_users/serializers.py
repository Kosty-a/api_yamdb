from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers

from .utils import generate_confirmation_code


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        confirmation_code = generate_confirmation_code()
        send_mail(
            subject='Confirmation code',
            message=confirmation_code,
            from_email='yamdb-no-reply@yamdb.com',
            recipient_list=[validated_data['email']]
        )
        return User.objects.create(
            **validated_data, confirmation_code=confirmation_code
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Invalid username')
        return value


class CustomUserSerializer_1(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CustomUserSerializer_2(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
