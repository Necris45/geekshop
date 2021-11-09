from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductCategory, Product
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.cache import cache

# Create your views here.


def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'products/index.html', context)


def get_links_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.filter(is_active=True)
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_link_product(category_id=None):
    if settings.LOW_CACHE:
        key = 'links_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = \
                Product.objects.filter(category_id=category_id, is_active=True,
                                       category__is_active=True).select_related('category') if category_id is not None \
                    else Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
        return link_product
    else:
        return Product.objects.filter(category_id=category_id, is_active=True,
                                      category__is_active=True).select_related('category') if category_id is not None \
            else Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Каталог'
        context['categories'] = get_links_category()

        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']

        # goods = Product.objects.filter(category_id=category_id, is_active=True, category__is_active=True).\
        #     select_related('category') if category_id is not None else \
        #     Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

        goods = get_link_product(category_id=category_id)

        paginator = Paginator(goods, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator

        return context
