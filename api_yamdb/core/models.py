from django.contrib.auth import get_user_model
from django.db import models

from core.constants import LENGHT_TEXT_FIELD, MAX_REPRESENTATION_LENGHT

User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    """
    Абстрактная модель для моделей Category и Genre.

    Добавляет идентификатор и сортировку по наименованию.
    """

    name = models.CharField(
        max_length=LENGHT_TEXT_FIELD,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_REPRESENTATION_LENGHT]


class ReviewCommentBaseModel(models.Model):
    """
    Абстрактная модель для моделей Review и Comment.


    Добавляет дату добавления отзыва или комментария и автора.
    """

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:MAX_REPRESENTATION_LENGHT]
