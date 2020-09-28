from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from authapp.models import ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        to_update = ShopUser.objects.filter(shopuserprofile__isnull=True)
        for user in to_update:
            ShopUserProfile.objects.create(user=user)
