from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser, LoginOtp, AuthorizationCode


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "auth_provider",
        "is_active",
        "is_staff",
        "date_joined",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

    list_filter = (
        "auth_provider",
        "is_active",
        "is_staff",
    )

    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Enterprise Information",
            {
                "fields": (
                    "phone",
                    "auth_provider",
                    "entra_object_id",
                    "entra_tenant_id",
                )
            },
        ),
    )


@admin.register(LoginOtp)
class LoginOtpAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "otp",
        "verified",
        "created_at",
        "expires_at",
    )

    search_fields = (
        "user__email",
    )
    
@admin.register(AuthorizationCode)
class AuthorizationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "user",
        "used",
        "expires_at",
    )

    search_fields = (
        "code",
        "user__email",
    )