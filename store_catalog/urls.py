"""store_catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core.autocomplete import ItemAutocompleteView
from core.views import \
    ItemDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('select2/item/',
         ItemAutocompleteView.as_view(),
         name='item-select2'),

    path('category/',
         CategoryListView.as_view(), name='categories'),
    path('category/<slug:category_slug>/',
         CategoryDetailView.as_view(), name='category'),
    path('category/<slug:category_slug>/<slug:item_slug>/',
         ItemDetailView.as_view(), name='item-detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
