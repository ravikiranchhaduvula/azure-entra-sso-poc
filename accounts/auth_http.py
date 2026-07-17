from django.conf import settings


def attach_auth_cookies(response, tokens):
    """
    Attach CapeArk authentication cookies
    to any HTTP response.
    """

    response.set_cookie(
        "capeark_access",
        tokens["access"],
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
    )

    response.set_cookie(
        "capeark_refresh",
        tokens["refresh"],
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
    )

    return response