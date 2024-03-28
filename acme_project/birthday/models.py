from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .validators import real_age

User = get_user_model()


class Tag(models.Model):
    tag = models.CharField('Тег', max_length=20)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        help_text='Необязательное поле',
        max_length=20
    )
    birthday = models.DateField('Дата рождения',  validators=(real_age,))
    image = models.ImageField(
        'Фото',
        upload_to='birthdays_images',
        blank=True
    )
    author = models.ForeignKey(
        User, verbose_name='Автор записи',
        on_delete=models.CASCADE,
        null=True,
        related_name='birthday'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    )

    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'День рождения'
        verbose_name_plural = 'Дни рождения'

    def __str__(self):
        return self.first_name


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
