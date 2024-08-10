from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Category.'''

    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_display_links = ('name',)


class GenreAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Genre.'''

    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_display_links = ('name',)


class TitlesAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Titles.'''

    list_display = ('id', 'name', 'year', 'category')
    list_editable = ('category',)
    search_fields = ('name',)
    filter_horizontal = ('genre',)
    list_display_links = ('name',)


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_editable = ('genre',)


class ReviewAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Review.'''

    list_display = ('title', 'text', 'score', 'author', 'pub_date')
    list_editable = ('text', 'author', 'score')
    search_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    '''Настройка админ-зоны для модели Comment.'''

    list_display = ('review', 'text', 'author', 'pub_date')
    list_editable = ('text', 'author')
    search_fields = ('text',)


admin.site.empty_value_display = 'Не задано'
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
