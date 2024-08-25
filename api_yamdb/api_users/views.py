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

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class ObtainTokenAPIView(APIView):

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        user = User.objects.get(username=username)
        refresh = RefreshToken.for_user(user)

        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


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
        data = request.data

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)

        return Response(serializer.data, status=status.HTTP_200_OK)
