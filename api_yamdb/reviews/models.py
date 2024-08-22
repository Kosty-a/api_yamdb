from datetime import date as dt

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.constants import (
    LENGHT_TEXT_FIELD, MAX_REPRESENTATION_LENGHT, MAX_SCORE, MIN_SCORE)
from core.models import CategoryGenreBaseModel, ReviewCommentBaseModel


User = get_user_model()


def year_validators(year):
    '''Функция проверяет, что год не более текущего.'''
    year_now = dt.today().year
    if year > year_now:
        raise ValidationError(
            'Год не может быть больше текущего.'
        )


class Category(CategoryGenreBaseModel):
    '''Модель категории произведений («Фильмы», «Книги», «Музыка»).

    Одно произведение может быть привязано только к одной категории.
    '''

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBaseModel):
    '''Модель жанров произведений.

    Одно произведение может быть привязано к нескольким жанрам.
    '''

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


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
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[year_validators]
    )
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
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_REPRESENTATION_LENGHT]

    def genre_names(self):
        return " %s" % (", ".join([genre.name for genre in self.genre.all()]))


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
        default_related_name = 'genretitles'
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        ordering = ('title',)

    def __str__(self):
        return f'У произведения "{self.title}" жанр "{self.genre}".'


class Review(ReviewCommentBaseModel):
    '''Модель отзывов на произведения.

    Отзыв привязан к определённому произведению.
    '''

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)
        ],
        verbose_name='Оценка'
    )

    class Meta(ReviewCommentBaseModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]


class Comment(ReviewCommentBaseModel):
    '''Модель комментариев к отзывам.

    Комментарий привязан к определённому отзыву.
    '''

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewCommentBaseModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
