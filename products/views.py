from django.shortcuts import render
from .models import ProductCategory, Product

# Create your views here.


def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'products/index.html', context)


def products(request):
    title = 'GeekShop - Каталог'
    goods = Product.objects.all()
    context = {
        'title': title,
        'categories': ProductCategory.objects.all(),
        'products': goods
    }
    return render(request, 'products/products.html', context)
