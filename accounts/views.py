import requests
from .models import AppUser
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import HttpResponse
from urllib.parse import urlencode
from .models import AppUser, LoginOtp
from .auth_tokens import generate_app_tokens
from .serializers import RegisterSerializer, LoginSerializer, VerifyOtpSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
import jwt
from .auth_http import attach_auth_cookies
from .auth_service import complete_login


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone": user.phone,
                        "auth_provider": user.auth_provider,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            otp = LoginOtp.generate_otp()

            LoginOtp.objects.create(
                user=user,
                otp=otp,
                expires_at=LoginOtp.expiry_time(),
            )

            print(f"OTP for {user.email}: {otp}")

            return Response(
                {
                    "message": "OTP generated successfully. Check Django console.",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login_otp = serializer.validated_data["login_otp"]
            
            login_otp.verified = True
            login_otp.save(update_fields=["verified"])
            
            auth = complete_login(user)
            
            api_response = Response(
                {
                    "message": "Login successful.",
                    "tokens": auth["tokens"],
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "auth_provider": user.auth_provider,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            attach_auth_cookies(api_response, auth["tokens"])
            return api_response
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntraStartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        params = {
            "client_id": settings.ENTRA_CLIENT_ID,
            "redirect_uri": settings.ENTRA_REDIRECT_URI,
            "response_type": "code",
            "response_mode": "query",
            "scope": "openid profile email",
            "state": "mock-state-123",
        }

        authorize_url = (
            f"https://login.microsoftonline.com/"
            f"{settings.ENTRA_TENANT_ID}"
            f"/oauth2/v2.0/authorize?"
            + urlencode(params)
        )
        print("##############", authorize_url)
        return redirect(authorize_url)
        
class EntraCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response(
                {"error": "Authorization code missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_response = requests.post(
            f"https://login.microsoftonline.com/{settings.ENTRA_TENANT_ID}/oauth2/v2.0/token",
            data={
                "client_id": settings.ENTRA_CLIENT_ID,
                "client_secret": settings.ENTRA_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.ENTRA_REDIRECT_URI,
                "scope": "openid profile email",
            },
            timeout=10,
        )

        token_response.raise_for_status()
        
        token_data = token_response.json()

        id_token = token_data["id_token"]
        
        claims = jwt.decode(
            id_token,
            options={"verify_signature": False},
            algorithms=["RS256"],
        )

        email = claims.get("preferred_username") or claims.get("email")
        name = claims.get("name")
        oid = claims.get("oid")
        tid = claims.get("tid")


        user, created = AppUser.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "first_name": name,
                "auth_provider": AppUser.AUTH_PROVIDER_ENTRA,
                "entra_object_id": oid,
                "entra_tenant_id": tid,
                "is_active": True,
            },
        )
        
        if not created:
            user.first_name = name
            user.auth_provider = AppUser.AUTH_PROVIDER_ENTRA
            user.entra_object_id = oid
            user.entra_tenant_id = tid
            user.save(
                update_fields=[
                    "first_name",
                    "auth_provider",
                    "entra_object_id",
                    "entra_tenant_id",
                ]
            )

        auth = complete_login(user)
        
        response = redirect(settings.DASHBOARD_URL)
        
        attach_auth_cookies(response, auth["tokens"])
        
        return response
        
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": "Welcome to TapeArk dashboard.",
                "user": {
                    "id": request.user.id,
                    "name": request.user.name,
                    "username": request.user.username,
                    "email": request.user.email,
                    "auth_provider": request.user.auth_provider,
                },
            },
            status=status.HTTP_200_OK,
        )
        
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(
            {"message": "Logged out successfully."},
            status=200,
        )

        response.delete_cookie("capeark_access")
        response.delete_cookie("capeark_refresh")

        return response