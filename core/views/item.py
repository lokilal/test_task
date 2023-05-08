from django.urls import reverse
from django.views.generic import DeleteView, DetailView
from django_filters.views import FilterView
from extra_views import (CreateWithInlinesView, NamedFormsetsMixin,
                         SuccessMessageMixin, UpdateWithInlinesView)

from core.filters import ItemFilterSet
from core.forms import ImageInline
from core.models import Category, Item
from core.views import AccessMixin


class ItemsInCategoryDetailView(AccessMixin, FilterView):
    template_name = 'core/item/items_list.html'
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


class ItemDetailView(AccessMixin, DetailView):
    template_name = 'core/item/item_detail.html'
    model = Item
    slug_url_kwarg = 'item_slug'


class ItemMixin(AccessMixin, SuccessMessageMixin, NamedFormsetsMixin):
    template_name = 'core/item/item_form.html'
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
    template_name = 'core/item/item_delete.html'
    slug_url_kwarg = 'item_slug'

    def get_success_url(self):
        return reverse('category-detail',
                       kwargs={'category_slug': self.object.category.slug})
