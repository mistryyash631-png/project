import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a default admin user from env vars."

    def handle(self, *args, **options):
        username = os.getenv("ADMIN_USERNAME", "Yash@gmail.com").strip()
        email = os.getenv("ADMIN_EMAIL", username).strip()
        password = os.getenv("ADMIN_PASSWORD", "Yash@123")

        if not username or not password:
            self.stdout.write(
                self.style.ERROR("ADMIN_USERNAME and ADMIN_PASSWORD are required.")
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Admin user created: {username}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Admin user updated: {username}")
            )
