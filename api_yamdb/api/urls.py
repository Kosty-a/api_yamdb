from django.urls import include, path

from .views import (CategoryDestroyAPIView, CategoryListCreateAPIView,
                    GenreDestroyAPIView, GenreListCreateAPIView)

urlpatterns = [
    path('', include('api_users.urls')),
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<slug:slug>/', CategoryDestroyAPIView.as_view()),
    path('genres/', GenreListCreateAPIView.as_view()),
    path('genres/<slug:slug>/', GenreDestroyAPIView.as_view()),
]
