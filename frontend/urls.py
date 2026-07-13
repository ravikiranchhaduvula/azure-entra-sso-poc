from django.urls import path
from .views import HomeView, DashboardView, OtpPageView

urlpatterns = [
    path("", HomeView.as_view(), name="login-page"),
    path("dashboard-page/", DashboardView.as_view(), name="dashboard-page"),
    path("otp-page/", OtpPageView.as_view(), name="otp-page"),
]