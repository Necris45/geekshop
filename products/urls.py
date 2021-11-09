from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ProductListView, ProductDetail

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='category'),
    path('page/<int:page_id>/', ProductListView.as_view(), name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
]
