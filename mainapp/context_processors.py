from .models import ProductCategory


def cat_menu(request):

    categories = ProductCategory.objects.all()
    return {
        'cat_menu': categories
    }
