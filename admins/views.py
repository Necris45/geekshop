from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import connection
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductCategoryCreateForm, ProductCreateForm, \
    OrderUpdateForm
from geekshop.mixin import CustomDispatchMixin
from ordersapp.models import Order
from users.models import User
from products.models import ProductCategory, Product
from django.shortcuts import render
from django.db.models import F
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


# Create your views here.
def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-read.html'
    success_url = reverse_lazy('admins:admins_user')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active is not False:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        return context


class CategoryCreateView(CreateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin_category_create.html'
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('admins:admins_categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Новая категория'
        return context


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('admins:admins_categories')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                # print(f'применяется скидка {discount} % к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Изменение Категории'
        return context


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    success_url = reverse_lazy('admins:admins_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active is not False:
            self.object.is_active = False
            # self.object.product_set.update(is_active=False)
        else:
            self.object.is_active = True
            # self.object.product_set.update(is_active=True)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Продукты'
        return context


class ProductCreateView(CreateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Новый товар'
        return context


class ProductUpdateView(UpdateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Изменение товара'
        return context


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    success_url = reverse_lazy('admins:admins_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active is not False:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class OrderListView(ListView, CustomDispatchMixin):
    model = Order
    template_name = 'admins/admin-orders-read.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Заказы'
        return context


class OrderUpdateView(UpdateView, CustomDispatchMixin):
    model = Order
    template_name = 'admins/admin-order-update-delete.html'
    form_class = OrderUpdateForm
    success_url = reverse_lazy('admins:admins_orders')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Изменение заказа'
        return context


class OrderDeleteView(DeleteView, CustomDispatchMixin):
    model = Order
    template_name = 'admins/admin-orders-read.html'
    success_url = reverse_lazy('admins:admins_orders')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active is not False:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
