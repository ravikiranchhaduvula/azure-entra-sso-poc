from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    VerifyOtpView,
    EntraStartView,
    EntraCallbackView,
    DashboardView,
    LogoutView,
    AuthorizationCodeExchangeView,
    CookieTokenRefreshView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/verify-otp/", VerifyOtpView.as_view()),

    path("auth/entra/start/", EntraStartView.as_view()),
    path("auth/entra/callback/", EntraCallbackView.as_view()),

    path("auth/dashboard/", DashboardView.as_view(), name="dashboard"),

    path(
        "auth/token/refresh/",
        CookieTokenRefreshView.as_view(),
        name="token-refresh",
    ),

    path("auth/logout/", LogoutView.as_view()),

    path(
        "auth/token/",
        AuthorizationCodeExchangeView.as_view(),
        name="authorization-code-exchange",
    ),
]