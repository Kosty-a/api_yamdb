from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnly


class CategoryAndGenreViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    '''Базовый вьюсет для моделей Category и Genre.'''

    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
