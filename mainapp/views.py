from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse


def get_hot_product():
    return Product.objects.all().order_by('?').first()


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).\
                                    exclude(pk=hot_product.pk)[:2]
    return same_products


def main(request):
    products = Product.objects.all().order_by('?')[:6]
    return render(request, 'mainapp/index.html',
    context={'title': 'home',
             'products': products,
             'main_menu': [{'href': 'index', 'name': 'home'},
                            {'href': 'showroom', 'name': 'showroom'},
                            {'href': 'contacts', 'name': 'contact'}
                           ]})


def products(request, pk=None, page=1):

    title = 'catalog'
    #categories = ProductCategory.objects.all()
    #basket = request.user.basket.all()[0] if request.user.is_authenticated else []

    if pk:
        if pk == '0':
            #Добавил к products = Product.objects.all()
            #products = Product.objects.all().order_by('?')[:6]
            products = Product.objects.filter(is_active=True).order_by('price')

            category = {'name': 'все',
                        'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            #products = Product.objects.filter(category__pk=pk).order_by('?')[:6]
            products = Product.objects.filter(category__pk=pk, is_active=True).order_by('price')

        paginator = Paginator(products, 12)
        try:
            products_paginator = paginator.page(page)
            print(len(products_paginator))
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context = {
            'title': title,
            #'cat_menu': categories,
            'category': category,
            'products': products_paginator,
            #'products': products,
        }

        return render(request, 'mainapp/catalog.html', context)

    hot_product = get_hot_product()

    same_products = get_same_products(hot_product)

    context = {
        'title': 'products',
        #'cat_menu': categories,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/hot_products.html', context)


def product(request, pk):

    title = 'product_detailes'
    #category = get_object_or_404(ProductCategory, pk=pk)
    context = {
        'title': title,
        #'cat_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        #'category': category,
    }
    if request.is_ajax():
        product = get_object_or_404(Product, pk=pk)
        return JsonResponse({'result': product.price})

    return render(request, 'mainapp/product_detailes.html', context)


def contact(request):
    return render(request, 'mainapp/contacts.html',
    context={'title': 'contacts'})


def showroom(request):
    return render(request, 'mainapp/showroom.html',
    context={'title': 'showroom'})

# Create your views here.
