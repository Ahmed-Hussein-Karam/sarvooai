from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates fake users for testing'

    def handle(self, *args, **options):
        users = [
            {'username': 'Bela', 'email': 'bela.safwat@gmail.com', 'password': 'Bela123'},
            {'username': 'Ahmed', 'email': 'ahkcsit@gmail.com', 'password': 'Ahmed123'},
        ]
        for user_data in users:
            username = user_data['username']
            email=user_data['email']
            password = user_data['password']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, email, password)
                self.stdout.write(self.style.SUCCESS(f"User '{username}' created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists"))
