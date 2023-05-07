from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, ListView
from django_filters.views import FilterView
from extra_views import (CreateWithInlinesView, NamedFormsetsMixin,
                         UpdateWithInlinesView)

from core.filters import ItemFilterSet
from core.forms import ImageInline
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


class ItemDetailView(AccessMixin, DetailView):
    template_name = 'core/item_detail.html'
    model = Item
    slug_url_kwarg = 'item_slug'


class CategoryListView(AccessMixin, ListView):
    template_name = 'core/categories.html'
    model = Category
    paginate_by = 30


class CategoryDetailView(AccessMixin, FilterView):
    template_name = 'core/items_list.html'
    model = Item
    filterset_class = ItemFilterSet
    paginate_by = 60

    def get_queryset(self):
        return super().get_queryset()\
            .filter(category__slug=self.kwargs.get('category_slug'))

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['category_slug'] = self.kwargs.get('category_slug')
        return kwargs


class ItemMixin(AccessMixin, SuccessMessageMixin, NamedFormsetsMixin):
    template_name = 'core/item_form.html'
    model = Item
    slug_url_kwarg = 'item_slug'
    fields = ['title', 'price', 'description', 'article', 'category']
    success_message = 'Сохранено'
    inlines = [ImageInline]
    inlines_names = ['image_formset']

    def get_form_class(self):
        form = super().get_form_class()
        if self.request.user.is_admin:
            category_qs = Category.objects.all()
        else:
            category_qs = self.get_allowed_categories()
        form.base_fields['category'].queryset = category_qs
        return form


class ItemUpdateView(ItemMixin, UpdateWithInlinesView):
    pass


class ItemCreateView(ItemMixin, CreateWithInlinesView):
    pass


class ItemDeleteView(AccessMixin, DeleteView):
    model = Item
    template_name = 'core/item_delete.html'
    slug_url_kwarg = 'item_slug'

    def get_success_url(self):
        return reverse('category',
                       kwargs={'category_slug': self.object.category.slug})
