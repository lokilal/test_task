from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class RoleChoice(models.IntegerChoices):
        MANAGER = 1, 'Менеджер'
        ADMIN = 2, 'Администратор'

    role = models.PositiveSmallIntegerField(
        choices=RoleChoice.choices, verbose_name='Роль',
        default=RoleChoice.MANAGER)
    allowed_categories = models.ManyToManyField(
        'core.Category', blank=True, verbose_name='Доступные категории')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.RoleChoice.ADMIN or self.is_superuser

    @property
    def is_manager(self):
        return self.role == self.RoleChoice.MANAGER
