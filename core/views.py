from django.views.generic import ListView, DetailView

from .models import Item

class ItemsListView(ListView):
    model = Item
    template_name = 'core/items_list.html'


class ItemDetailView(DetailView):
    template_name = 'core/item_detail.html'
    model = Item
