from django.urls import path
from .views import HomeView, DashboardView, OtpPageView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login-page/", HomeView.as_view(), name="login-page"),

    path("otp-page/", OtpPageView.as_view(), name="otp-page"),
    path("dashboard-page/", DashboardView.as_view(), name="dashboard-page"),
]