from django.utils import timezone

from .auth_tokens import generate_app_tokens


def complete_login(user):
    """
    Common authentication logic used by
    OTP login and Entra login.
    """

    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])

    tokens = generate_app_tokens(user)

    return {
        "user": user,
        "tokens": tokens,
    }