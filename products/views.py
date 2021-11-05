from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductCategory, Product
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy


# Create your views here.


def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'products/index.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Каталог'
        context['categories'] = ProductCategory.objects.filter(is_active=True)

        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']

        goods = Product.objects.filter(category_id=category_id, is_active=True, category__is_active=True).\
            select_related('category') if category_id is not None else \
            Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

        paginator = Paginator(goods, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator

        return context
