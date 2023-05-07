from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from extra_views import UpdateWithInlinesView, NamedFormsetsMixin

from core.forms import ImageInline
from core.filters import ItemFilterSet
from core.models import Item, Category

from django.contrib.messages.views import SuccessMessageMixin

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
            elif self.model is Category:
                return self.get_allowed_categories()
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


class ItemUpdateView(AccessMixin, SuccessMessageMixin, NamedFormsetsMixin,
                     UpdateWithInlinesView):
    template_name = 'core/item_update.html'
    model = Item
    slug_url_kwarg = 'item_slug'
    fields = ['title', 'price', 'description', 'article', 'category']
    success_message = 'Сохранено'
    inlines = [ImageInline]
    inlines_names = ['image_formset']

    def get_form_class(self):
        form = super().get_form_class()
        form.base_fields['category'].queryset = self.get_allowed_categories()
        return form

