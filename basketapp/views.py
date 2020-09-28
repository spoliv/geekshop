from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse, reverse
from django.contrib.auth.decorators import login_required
from .models import Basket
from mainapp.models import Product

from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket(request):

    basket_items = request.user.basket.all()
    return render(request, 'basketapp/basket.html', context={
        'basket_items': basket_items
    })


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket = request.user.basket.filter(pk=pk).first()

    if basket:
        if basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
        else:
            basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        basket_item = get_object_or_404(Basket, pk=int(pk))
        quantity = int(quantity)
        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket_items': basket_items,
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', context)
        # result = 'ok'
        return JsonResponse({
            'result': result
        })

# Create your views here.
