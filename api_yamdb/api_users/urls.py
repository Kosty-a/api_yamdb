from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ObtainTokenAPIView, SignUpAPIView, UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view()),
    path('auth/token/', ObtainTokenAPIView.as_view()),
    path('', include(router.urls)),
]
