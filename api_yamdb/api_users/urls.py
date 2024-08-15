from django.urls import path

from .views import (CustomUserListCreateAPIView,
                    CustomUserRetrieveUpdateAPIView,
                    CustomUserRetrieveUpdateDestroyAPIView, GetTokenAPIView,
                    SignUpAPIView)

urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view()),
    path('auth/token/', GetTokenAPIView.as_view()),
    path('users/', CustomUserListCreateAPIView.as_view()),
    path('users/me/', CustomUserRetrieveUpdateAPIView.as_view()),
    path('users/<username>/', CustomUserRetrieveUpdateDestroyAPIView.as_view())
]
