from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import render

class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "login.html")


class DashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "dashboard.html")
        
class OtpPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "otp.html")