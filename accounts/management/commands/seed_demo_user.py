from django.core.management.base import BaseCommand
from accounts.models import AppUser
import os


class Command(BaseCommand):
    help = "Creates a demo user if it does not already exist."

    def handle(self, *args, **kwargs):
        email = os.getenv(
            "DEMO_USER_EMAIL",
            "ravi@example.com",
        )

        username = os.getenv(
            "DEMO_USER_USERNAME",
            "ravik",
        )

        first_name = os.getenv(
            "DEMO_USER_FIRST_NAME",
            "Ravi",
        )

        last_name = os.getenv(
            "DEMO_USER_LAST_NAME",
            "Kiran",
        )

        password = os.getenv(
            "DEMO_USER_PASSWORD",
            "Password123!",
        )

        if AppUser.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.SUCCESS(
                    "Demo user already exists."
                )
            )
            return

        AppUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo user created successfully."
            )
        )