from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_users.permissions import IsAdminOrSuperUser
from api_users.serializers import (ObtainTokenSerializer, SignUpSerializer,
                                   UserSerializer)


User = get_user_model()


class SignUpAPIView(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenAPIView(APIView):

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=serializer.data['username'])
            if user.confirmation_code == serializer.data['confirmation_code']:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK
                )

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'patch', 'delete', 'list', 'post')
    lookup_field = 'username'
    queryset = User.objects.all()

    @action(methods=('get', 'patch'), detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        user = request.user
        data = request.data.copy()

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if 'role' in data:
            data.pop('role')

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
