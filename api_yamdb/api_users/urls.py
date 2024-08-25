from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_users.views import ObtainTokenAPIView, SignUpAPIView, UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUpAPIView.as_view()),
    path('v1/auth/token/', ObtainTokenAPIView.as_view()),
    path('v1/', include(router.urls)),
]
