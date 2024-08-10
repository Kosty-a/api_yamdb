from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.exceptions import NotFound
from reviews.models import Category, Genre, Review, Title

from api.core import CategoryAndGenreViewSet
from api.permissions import (
    AdminOrReadOnly, IsAdminOrModeratorOrReadOnly
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ListDetailTitleSerializer, ReviewSerializer, TitleSerializer
)


class CategoryViewSet(CategoryAndGenreViewSet):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryAndGenreViewSet):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    #queryset = (Title.objects.all().annotate(Avg('review__score')).order_by('name'))
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return ListDetailTitleSerializer
        return TitleSerializer


class ReviewViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrReadOnly, IsAuthenticated)
    http_method_names = ["get", "post", "patch", "delete"]

    def _get_title_or_404(self):
        """Метод получает произведение по title_id либо 404,
        если такого произведения не существует.
        """
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self._get_title_or_404().review.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self._get_title_or_404()
        )


class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrReadOnly,)
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
