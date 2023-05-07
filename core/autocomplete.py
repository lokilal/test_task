from dal_select2.views import Select2QuerySetView

from core.models import Item


class ItemAutocompleteView(Select2QuerySetView):
    model = Item

    def get_result_value(self, result):
        if self.request.GET.get('field'):
            return getattr(result, self.request.GET.get('field'))
        return super().get_result_value(result)

    def get_result_label(self, result):
        if self.request.GET.get('field'):
            return getattr(result, self.request.GET.get('field'))
        return super().get_result_value(result)

    def get_search_fields(self):
        if self.request.GET.get('field'):
            return [self.request.GET.get('field')]
        return ['title', 'article', 'price', 'description']

    def get_queryset(self):
        if self.request.GET.get('category'):
            return self.model.objects\
                .filter(category__slug=self.request.GET.get('category'))
        return self.model.objects.all()
