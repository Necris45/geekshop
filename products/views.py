from django.shortcuts import render
from .models import ProductCategory, Product

# Create your views here.


def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'products/index.html', context)


def products(request, pk=None):
    if 1 <= pk <= 5:
        title = ProductCategory.objects.get(id=pk)
        print(title)
        products = Product.objects.filter(category=title)
    else:
        title = 'GeekShop - Каталог'
        products = Product.objects.all()
    context = {
        'title': title,
        'products': products
    }
    return render(request, 'products/products.html', context)
