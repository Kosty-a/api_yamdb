from rest_framework import serializers
from reviews.models import Category, Genre


class CategoryListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CategoryDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug',)


class GenreListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class GenreDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('slug',)
