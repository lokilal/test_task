from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from django.db.models import Q

from core.models import Item, Category
from core.filters import ItemFilterSet


class AccessMixin:
    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            allowed_categories_ids = \
                user.allowed_categories.values_list('id', flat=True)

            q = Q()
            if self.model is Item:
                q = Q(category__in=allowed_categories_ids)
            elif self.model is Category:
                q = Q(id__in=allowed_categories_ids)

            return super().get_queryset()\
                .filter(q)
        elif user.is_admin:
            return super().get_queryset()


class ItemDetailView(AccessMixin, DetailView):
    template_name = 'core/item_detail.html'
    model = Item
    slug_url_kwarg = 'item_slug'


class CategoryListView(AccessMixin, ListView):
    template_name = 'core/categories.html'
    model = Category


class CategoryDetailView(AccessMixin, FilterView):
    template_name = 'core/items_list.html'
    model = Item
    filterset_class = ItemFilterSet

    def get_queryset(self):
        return super().get_queryset()\
            .filter(category__slug=self.kwargs.get('category_slug'))

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['category_slug'] = self.kwargs.get('category_slug')
        return kwargs
