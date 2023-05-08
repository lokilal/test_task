from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.models import Category
from core.views.mixins import AccessMixin, OnlyAdminMixin


class CategoryListView(AccessMixin, ListView):
    template_name = 'core/category/category_list.html'
    model = Category
    paginate_by = 30


class CategoryCreateView(OnlyAdminMixin, CreateView):
    model = Category
    template_name = 'core/category/category_form.html'
    success_url = reverse_lazy('category-list')
    fields = ['title']


class CategoryUpdateView(OnlyAdminMixin, UpdateView):
    model = Category
    template_name = 'core/category/category_form.html'
    slug_url_kwarg = 'category_slug'
    success_url = reverse_lazy('category-list')
    fields = ['title']


class CategoryDeleteView(OnlyAdminMixin, DeleteView):
    model = Category
    template_name = 'core/category/category_delete.html'
    slug_url_kwarg = 'category_slug'
    success_url = reverse_lazy('category-list')
