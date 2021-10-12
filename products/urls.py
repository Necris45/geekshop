from django.urls import path
from .views import ProductListView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='category'),
    path('page/<int:page_id>/', ProductListView.as_view(), name='page'),
]
