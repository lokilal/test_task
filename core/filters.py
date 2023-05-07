from urllib.parse import urljoin

from dal import autocomplete
from django.urls import reverse
from django_filters import FilterSet, CharFilter

from core.models import Item


class ItemFilterSet(FilterSet):
    class Meta:
        model = Item
        fields = ['title', 'price', 'article', 'description']

    def __init__(self, *args, **kwargs):
        category_slug = kwargs.pop('category_slug')
        super().__init__(*args, **kwargs)
        for filter_name in self.filters.keys():
            query_parameters = f'?field={filter_name}&category={category_slug}'
            absolute_url = urljoin(reverse('item-select2'), query_parameters)
            self.filters[filter_name].field.widget = \
                autocomplete.Select2(url=absolute_url)
