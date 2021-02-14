from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = os.getenv('ADMIN_USER')
        mail = os.getenv('ADMIN_MAIL')
        password = os.getenv('ADMIN_PASSWORD')
        User.objects.create_superuser(username=user, email=mail, password=password)