from rest_framework_simplejwt.tokens import RefreshToken


def generate_app_tokens(user):
    refresh = RefreshToken.for_user(user)

    refresh["email"] = user.email
    refresh["username"] = user.username
    refresh["auth_provider"] = user.auth_provider

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }