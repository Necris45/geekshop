from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductCategory, Product

# Create your views here.


def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_id=1):
    title = 'GeekShop - Каталог'
    goods = Product.objects.filter(category_id=category_id, is_active=True, category__is_active=True) if category_id != None \
        else Product.objects.filter(is_active=True, category__is_active=True)

    paginator = Paginator(goods, per_page=3)
    try:
        goods_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        goods_paginator = paginator.page(1)
    except EmptyPage:
        goods_paginator = paginator.page(paginator.num_pages)
    context = {
        'title': title,
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': goods_paginator
    }
    return render(request, 'products/products.html', context)
