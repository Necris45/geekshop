from django.shortcuts import render

# Create your views here.


def login(request):
    context = {
        'title': 'GeekShop - Авторизация'
    }
    return render(request, 'users/login.html', context)


def register(request):
    context = {
        'title': 'GeekShop - Регистрация'
    }
    return render(request, 'users/register.html', context)
