from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from mainapp.models import ProductCategory
from authapp.models import ShopUser
from mainapp.models import Product
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Список категорий'
        return context


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание категории'
        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение категории'
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление категории'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ShopUserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, **kwargs):
        context = super(ShopUserListView, self).get_context_data(**kwargs)
        context['title'] = 'Список пользователей'
        return context


class ShopUserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание пользователя'
        return context


class ShopUserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение профиля пользователя'
        return context


class ShopUserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление пользователя'
        return context

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(ShopUser, pk=kwargs['pk'])
        user.is_active = False
        user.save()
        return HttpResponseRedirect(self.success_url)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Продукты категории'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание продукта'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение продукта'
        return context


# class ProductDeleteView(DeleteView):
#     model = Product
#     template_name = 'adminapp/product_delete.html'
#     fields = '__all__'
#     success_url = reverse_lazy('admin_custom:products')
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDeleteView, self).get_context_data(**kwargs)
#         context['title'] = 'Удаление продукта'
#         return context

def product_delete(request, pk):
    print('ok')
    object = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('admin_custom:products',
                                            kwargs={'pk': object.category.pk}))
    context = {
        'title': 'продукты/удаление',
        'object': object,
        'category': object.category
    }
    return render(request, 'adminapp/product_delete.html', context)
# Create your views here.
