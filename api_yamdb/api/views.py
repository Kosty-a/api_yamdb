from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404

from api.core import CategoryAndGenreViewSet
from api.filters import TitleFilter
from api.permissions import (AdminOrReadOnly,
                             IsAdminOrModeratorOrAuthorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ListDetailTitleSerializer,
                             ReviewSerializer, TitleSerializer)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(CategoryAndGenreViewSet):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryAndGenreViewSet):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ListDetailTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]

    def _get_title_or_404(self):
        """Метод получает произведение по title_id либо 404,
        если такого произведения не существует.
        """
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self._get_title_or_404().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self._get_title_or_404()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]

    def _get_review_or_404(self):
        """Метод получает отзыв по review_id либо 404,
        если такого отзыва не существует.
        """
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self._get_review_or_404().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self._get_review_or_404()
        )
