from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AppUser, LoginOtp


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = AppUser

        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "password",
        )

    def validate_email(self, value):
        if AppUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )

        return value.lower().strip()

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = AppUser.objects.create_user(
            **validated_data
        )

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
    )

    def validate(self, data):

        user = authenticate(
            username=data["email"],
            password=data["password"],
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )

        data["user"] = user

        return data


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    otp = serializers.CharField(
        max_length=6,
    )

    def validate(self, data):

        email = data["email"]
        otp = data["otp"]

        try:
            user = AppUser.objects.get(
                email=email,
                is_active=True,
            )

        except AppUser.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid email or OTP."
            )

        login_otp = (
            LoginOtp.objects.filter(
                user=user,
                otp=otp,
                verified=False,
                expires_at__gt=timezone.now(),
            )
            .order_by("-created_at")
            .first()
        )

        if login_otp is None:
            raise serializers.ValidationError(
                "Invalid or expired OTP."
            )

        data["user"] = user
        data["login_otp"] = login_otp

        return data
        
class AuthorizationCodeExchangeSerializer(serializers.Serializer):
    code = serializers.CharField()