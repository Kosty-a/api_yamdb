from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters, generics
from rest_framework.exceptions import NotFound
from reviews.models import Category, Genre

from .permissions import AdminOrReadOnly
from .serializers import (CategoryDestroySerializer,
                          CategoryListCreateSerializer, GenreDestroySerializer,
                          GenreListCreateSerializer)


class CategoryGenreBaseListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryListCreateAPIView(CategoryGenreBaseListCreateAPIView):
    serializer_class = CategoryListCreateSerializer
    queryset = Category.objects.all()


class GenreListCreateAPIView(CategoryGenreBaseListCreateAPIView):
    serializer_class = GenreListCreateSerializer
    queryset = Genre.objects.all()


class CategoryGenreBaseDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (AdminOrReadOnly,)
    model = None

    def get_object(self):
        slug = self.kwargs.get('slug')
        try:
            obj = self.model.objects.filter(slug=slug)
            return obj
        except ObjectDoesNotExist:
            raise NotFound(detail='Not Found', code=404)


class CategoryDestroyAPIView(CategoryGenreBaseDestroyAPIView):
    serializer_class = CategoryDestroySerializer
    model = Category


class GenreDestroyAPIView(CategoryGenreBaseDestroyAPIView):
    serializer_class = GenreDestroySerializer
    model = Genre
