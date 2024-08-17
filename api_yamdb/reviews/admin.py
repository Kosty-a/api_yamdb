from django.contrib import admin

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Category.'''

    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_display_links = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Genre.'''

    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_display_links = ('name',)


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Titles.'''

    list_display = ('id', 'name', 'year', 'category', 'genre_names')
    list_editable = ('category',)
    search_fields = ('name',)
    filter_horizontal = ('genre',)
    list_display_links = ('name',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_editable = ('genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Review.'''

    list_display = ('title', 'text', 'score', 'author', 'pub_date')
    list_editable = ('text', 'author', 'score')
    search_fields = ('text',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Comment.'''

    list_display = ('review', 'text', 'author', 'pub_date')
    list_editable = ('text', 'author')
    search_fields = ('text',)


admin.site.empty_value_display = 'Не задано'
