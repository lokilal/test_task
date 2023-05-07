from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(
        max_length=128, verbose_name='Название')
    slug = AutoSlugField(
        populate_from='title', unique=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Item(models.Model):
    title = models.CharField(
        max_length=128, verbose_name='Наименование')
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=16, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='items', verbose_name='Категория')
    article = models.CharField(
        max_length=128, verbose_name='Артикул товара')
    description = models.TextField(
        verbose_name='Описание')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    slug = AutoSlugField(
        populate_from='title', unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('item-detail',
                       kwargs={'category_slug': self.category.slug,
                               'item_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class Image(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        related_name='images', verbose_name='Товар')
    image = models.ImageField(
        upload_to='images/', blank=True,
        verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
