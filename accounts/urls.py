from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, VerifyOtpView, EntraStartView, EntraCallbackView, DashboardView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
    path("auth/entra/start/", EntraStartView.as_view()),
    path("auth/entra/callback/", EntraCallbackView.as_view()),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view()),
]