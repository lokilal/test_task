from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from core.models import Category, Item


class AccessMixin(LoginRequiredMixin):

    def get_allowed_categories(self):
        allowed_categories_ids = self.request.user.allowed_categories\
            .values_list('id', flat=True)
        return Category.objects.filter(id__in=allowed_categories_ids)

    def get_allowed_items(self):
        allowed_categories_ids = self.request.user.allowed_categories\
            .values_list('id', flat=True)
        return Item.objects.filter(category__in=allowed_categories_ids)

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            if self.model is Item:
                return self.get_allowed_items()
            return self.get_allowed_categories()
        return super().get_queryset()


class OnlyAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin
