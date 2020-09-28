from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser

import json
import os

JSON_PATH = 'mainapp/json'


def loadFromJSON(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = loadFromJSON('categories')
        ProductCategory.objects.all().delete()
        [ProductCategory.objects.create(**category) for category in categories]
        products = loadFromJSON('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            Product.objects.create(**product)

        # Создаем суперпользователя при помощи менеджера модели
        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=53)
