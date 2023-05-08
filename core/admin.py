from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import Category, Image, Item, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительно', {'fields': (
            'role',
            'allowed_categories'
        )}),
    )
    list_filter = BaseUserAdmin.list_filter + ('role', )


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['title', 'article']
    inlines = [ImageInline]
    list_filter = ['category']
    list_display = ['title', 'article', 'price']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'slug']
