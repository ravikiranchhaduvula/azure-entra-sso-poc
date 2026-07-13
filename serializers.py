from rest_framework import serializers
from .models import AppUser


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)

    def validate_email(self, value):
        if AppUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def create(self, validated_data):
        return AppUser.objects.create(
            email=validated_data["email"],
            name=validated_data["name"],
            phone=validated_data.get("phone", ""),
            auth_provider=AppUser.AUTH_PROVIDER_NORMAL,
        )