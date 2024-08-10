from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (
    LENGHT_SLUG_FIELD, LENGHT_TEXT_FIELD, MAX_REPRESENTATION_LENGHT
)

User = get_user_model()


class Category(models.Model):
    '''Модель категории произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории.
    '''

    name = models.CharField(
        max_length=LENGHT_TEXT_FIELD,
        verbose_name='Категория'
    )
    slug = models.CharField(
        max_length=LENGHT_SLUG_FIELD,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        default_related_name = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name[:MAX_REPRESENTATION_LENGHT]


class Genre(models.Model):
    '''Модель жанров произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    '''

    name = models.CharField(
        max_length=LENGHT_TEXT_FIELD,
        verbose_name='Жанр'
    )
    slug = models.CharField(
        max_length=LENGHT_SLUG_FIELD,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        default_related_name = 'genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name[:MAX_REPRESENTATION_LENGHT]


class Title(models.Model):
    '''Модель произведений, к которым пишут отзывы.
    Определённый фильм, книга или песенка.
    Нельзя добавлять произведения, которые еще не вышли
    (год выпуска не может быть больше текущего).
    При добавлении нового произведения требуется указать
    уже существующие категорию и жанр.
    '''

    name = models.CharField(
        max_length=LENGHT_TEXT_FIELD,
        verbose_name='Произведение'
    )
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'title'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_REPRESENTATION_LENGHT]


class GenreTitle(models.Model):
    '''Модель жанров (Genre) и произведений (Title).
    Связь между моделями ManyToMany.
    '''

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        default_related_name = 'genretitle'
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        ordering = ('title',)

    def __str__(self):
        return f'У произведения "{self.title}" жанр "{self.genre}".'


class Review(models.Model):
    '''Модель отзывов на произведения.
    Отзыв привязан к определённому произведению.
    '''

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления отзыва и оценки'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )

    class Meta:
        default_related_name = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:MAX_REPRESENTATION_LENGHT]


class Comment(models.Model):
    '''Модель комментариев к отзывам.
    Комментарий привязан к определённому отзыву.
    '''

    text = models.TextField(verbose_name='Текст комментария')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:MAX_REPRESENTATION_LENGHT]
