from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView
# Create your views here.
from baskets.models import Basket
from geekshop.mixin import UserDispatchMixin
from products.models import Product


class BasketCreateView(CreateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'products/products.html'
    success_url = reverse_lazy('products:index')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'product_id' in kwargs:
            product_id = kwargs['product_id']
            if product_id:
                product = Product.objects.get(id=product_id)
                baskets = Basket.objects.filter(user=request.user, product=product)
                if not baskets.exists():
                    Basket.objects.create(user=request.user, product=product, quantity=1)
                else:
                    basket = baskets.first()
                    basket.quantity += 1
                    basket.save()

        return redirect(self.success_url)


class BasketDeleteView(DeleteView, UserDispatchMixin):
    model = Basket
    success_url = reverse_lazy('users:profile')


class BasketUpdateView(UpdateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    pk_url_kwarg = 'basket_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(BasketUpdateView, self).get_context_data(**kwargs)
    #     context['baskets'] = Basket.objects.filter(user=self.request.user)
    #     return context

    def get(self, request, *args, **kwargs):
        super(BasketUpdateView, self).get(request, *args, **kwargs)
        if request.is_ajax():
            basket_id = kwargs[self.pk_url_kwarg]
            quantity = kwargs['quantity']
            baskets = Basket.objects.filter(id=basket_id)
            if baskets.exists():
                basket = baskets.first()
                if quantity > 0:
                    basket.quantity = quantity
                    basket.save()
                else:
                    basket.delete()

            result = render_to_string('baskets/baskets.html', self.get_context_data(*args, **kwargs), request=request)

            return JsonResponse({'result': result})

        return redirect(self.success_url)
