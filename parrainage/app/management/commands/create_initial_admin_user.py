import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Créer un utilisateur admin initial"

    def handle(self, *args, **options):

        User = get_user_model()
        if User.objects.exists():
            return

        username = os.environ["ADMIN_USERNAME"]
        password = os.environ["ADMIN_PASSWORD"]
        email = os.environ["ADMIN_EMAIL"]

        User.objects.create_superuser(username=username, password=password, email=email)

        self.stdout.write(f'Initial user "{username}" was created')
