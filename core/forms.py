from django import forms
from extra_views import InlineFormSetFactory

from core.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class ImageInline(InlineFormSetFactory):
    model = Image
    form_class = ImageForm
    factory_kwargs = {'extra': 1}
