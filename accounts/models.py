import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class AppUser(AbstractUser):
    AUTH_PROVIDER_NORMAL = "NORMAL"
    AUTH_PROVIDER_ENTRA = "ENTRA"

    AUTH_PROVIDER_CHOICES = [
        (AUTH_PROVIDER_NORMAL, "Normal Login"),
        (AUTH_PROVIDER_ENTRA, "Microsoft Entra"),
    ]

    # Email will be our unique login
    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    phone = models.CharField(max_length=30, blank=True, null=True)

    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDER_CHOICES,
        default=AUTH_PROVIDER_NORMAL,
    )

    entra_object_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    entra_tenant_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.auth_provider})"

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower().strip()

        super().save(*args, **kwargs)        

    @property
    def name(self):
        return " ".join(
            filter(None, [self.first_name, self.last_name])
        )    

    class Meta:
        ordering = ["email"]

class LoginOtp(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name="login_otps",
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    verified = models.BooleanField(default=False)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def expiry_time():
        return timezone.now() + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"