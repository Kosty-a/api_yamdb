from datetime import date as dt

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ListDetailTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при GET-запросе."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        '''Функция получает среднее значение оценки рейтинга.'''
        return obj.review.aggregate(Avg('score'))['score__avg']

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    def validate_year(self, value):
        '''Функция проверяет, что год не более текущего.'''
        year = dt.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего.'
            )
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def create(self, validated_data):
        '''Функция проверяет, что автор ранее не оставлял отзыв
        на данное произведение.
        '''
        title = validated_data.get('title')
        author = validated_data.get('author')
        try:
            Review.objects.get(title=title, author=author)
            raise serializers.ValidationError('Review already exists')
        except ObjectDoesNotExist:
            return Review.objects.create(**validated_data)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
