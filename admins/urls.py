"""geekshop URL Configuration

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

from django.urls import path
from django.views.decorators.cache import cache_page

from .views import index, UserUpdateView, UserCreateView, UserListView, UserDeleteView, CategoryListView, \
    ProductListView, CategoryCreateView, ProductCreateView, CategoryUpdateView, CategoryDeleteView, ProductUpdateView, \
    ProductDeleteView, OrderListView

app_name = 'admins'
urlpatterns = [

    path('', index, name='index'),
    path('users/', cache_page(3600)(UserListView.as_view()), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),
    path('categories/', cache_page(3600)(CategoryListView.as_view()), name='admins_categories'),
    path('products/', cache_page(3600)(ProductListView.as_view()), name='admins_products'),
    path('category-create/', CategoryCreateView.as_view(), name='admins_category_create'),
    path('product-create/', ProductCreateView.as_view(), name='admins_product_create'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='admins_category_update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='admins_category_delete'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='admins_product_update'),
    path('product-delete/<int:pk>/', ProductDeleteView.as_view(), name='admins_product_delete'),
    path('orders/', cache_page(3600)(OrderListView.as_view()), name='admins_orders'),
]
