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

            user.last_login = timezone.now()
            print(type(user))
            print(user.__class__)
            print(user._meta.label)
            user.save(update_fields=["last_login"])

            tokens = generate_app_tokens(user)

            return Response(
                {
                    "message": "Login successful.",
                    "tokens": tokens,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "auth_provider": user.auth_provider,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class EntraStartView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        params = {
            "client_id": "mock-client-id",
            "redirect_uri": "http://127.0.0.1:8000/api/auth/entra/callback/",
            "response_type": "code",
            "scope": "openid profile email",
            "state": "mock-state-123",
        }

        authorize_url = "http://127.0.0.1:9000/authorize?" + urlencode(params)

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
            "http://127.0.0.1:9000/token",
            data={
                "code": code
            },
            timeout=5,
        )

        token_data = token_response.json()

        id_token = token_data["id_token"]

        email = id_token["email"]
        name = id_token["name"]
        oid = id_token["oid"]
        tid = id_token["tid"]


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
            user.last_login = timezone.now()
            user.save(
                update_fields=[
                    "first_name",
                    "auth_provider",
                    "entra_object_id",
                    "entra_tenant_id",
                    "last_login",
                ]
            )

        tokens = generate_app_tokens(user)
        
        html = f"""
<!DOCTYPE html>
<html>

<head>
    <title>CapeArk</title>

    <style>

        body {{
            font-family: Arial;
            background:#f5f5f5;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }}

        .card {{
            background:white;
            width:500px;
            padding:40px;
            border-radius:10px;
            box-shadow:0 2px 10px rgba(0,0,0,.15);
            text-align:center;
        }}

        button {{
            background:#0078D4;
            color:white;
            border:none;
            padding:12px 24px;
            border-radius:5px;
            cursor:pointer;
            font-size:16px;
        }}

    </style>

</head>

<body>

<div class="card">

<h2>Authentication Successful</h2>

<p>
Welcome <strong>{user.name}</strong>
</p>

<p>
Authentication Provider:
<strong>{user.auth_provider}</strong>
</p>

<p>
JWT tokens have been generated successfully.
</p>

<button onclick="window.location='/api/dashboard/'">

Open Dashboard

</button>

</div>

</body>

</html>
"""

        return HttpResponse(html)

        
        
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