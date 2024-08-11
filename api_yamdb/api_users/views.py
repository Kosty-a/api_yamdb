from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_users.permissions import IsAdminOrSuperUser
from api_users.serializers import (CustomUserSerializer_1,
                                   CustomUserSerializer_2, SignUpSerializer)
from api_users.utils import generate_confirmation_code

User = get_user_model()


class SignUpAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        try:
            user = User.objects.get(username=username)
            if user.email != email:
                return Response(
                    {'Error': 'Invalid email for user'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            confirmation_code = generate_confirmation_code()
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                subject='Confirmation code',
                message=confirmation_code,
                from_email='yamdb-no-reply@yamdb.com',
                recipient_list=[user.email]
            )
            return Response(
                {
                    'email': user.email,
                    'username': user.username
                },
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not username:
            return Response(
                {'Error': 'Username field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(
                {'Error': 'User does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.confirmation_code == confirmation_code:
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'Error': 'Invalid confirmation code'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomUserListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer_1
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    queryset = User.objects.all()


class CustomUserRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = CustomUserSerializer_1
    permission_classes = (IsAdminOrSuperUser,)
    http_method_names = ('get', 'patch', 'delete')

    def get_object(self):
        username = self.kwargs.get('username')
        try:
            user = User.objects.get(username=username)
            return user
        except ObjectDoesNotExist:
            raise NotFound(detail='User not found', code=404)


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer_2
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
