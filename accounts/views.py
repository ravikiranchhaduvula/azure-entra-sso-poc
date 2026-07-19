import requests
import base64
import json
from .models import AppUser
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import HttpResponse
from urllib.parse import urlencode
from .models import AppUser, LoginOtp, AuthorizationCode
from .auth_tokens import generate_app_tokens
from .serializers import RegisterSerializer, LoginSerializer, VerifyOtpSerializer, AuthorizationCodeExchangeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
import jwt
from .auth_http import attach_auth_cookies
from .auth_service import complete_login
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny


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

        # 🌽 Corn #2 - Remember where the login started
        return_url = request.GET.get("returnUrl")

        state = "default"
        
        if (
            return_url
            and return_url in settings.ALLOWED_RETURN_URLS
        ):

            state = base64.urlsafe_b64encode(
                json.dumps(
                    {
                        "return_url": return_url
                    }
                ).encode()
            ).decode()

            print("🌽 Encoded state:", state)

        else:

            print("❌ Invalid returnUrl:", return_url)

        params = {
            "client_id": settings.ENTRA_CLIENT_ID,
            "redirect_uri": settings.ENTRA_REDIRECT_URI,
            "response_type": "code",
            "response_mode": "query",
            "scope": "openid profile email",
            "state": state,
        }

        authorize_url = (
            f"https://login.microsoftonline.com/"
            f"{settings.ENTRA_TENANT_ID}"
            f"/oauth2/v2.0/authorize?"
            + urlencode(params)
        )

        print("Authorization URL:", authorize_url)

        return redirect(authorize_url)
        
class EntraCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        print("🔵 Callback Session Key:", request.session.session_key)
        print("🔵 Callback Session Data:", dict(request.session))
        
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
        
        authorization_code = AuthorizationCode.create_for_user(user)

        print("🥬 Authorization Code:", authorization_code.code)
        
        # 🌽 Retrieve the saved return URL
        state = request.GET.get("state")
         
        return_url = None

        if state:
    
           try:

              payload = json.loads(
                  base64.urlsafe_b64decode(state).decode()
              )

              return_url = payload.get("return_url")

              print("🌽 Return URL from state:", return_url)

           except Exception as ex:

               print("❌ Invalid state:", ex)            

        if return_url:
           redirect_url = (
               f"{return_url}?"
               + urlencode({"code": authorization_code.code})
           )

           print("🌽 Redirecting back to:", redirect_url)

           response = redirect(redirect_url)
        else:
            print("🌽 No returnUrl found. Redirecting to dashboard.")
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

    def _logout(self, request):

        return_url = request.GET.get("returnUrl")

        print("Logout returnUrl:", return_url)
        print("Allowed:", settings.ALLOWED_RETURN_URLS)

        if (
            return_url
            and return_url in settings.ALLOWED_RETURN_URLS
        ):
            response = redirect(return_url)
        else:
            response = redirect(settings.DASHBOARD_URL)

        response.delete_cookie(settings.ACCESS_COOKIE_NAME)
        response.delete_cookie(settings.REFRESH_COOKIE_NAME)

        return response

    def get(self, request):
        return self._logout(request)

    def post(self, request):
        return self._logout(request)

        
class AuthorizationCodeExchangeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = AuthorizationCodeExchangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        print("🥬 Exchange request:", code)

        try:
            authorization_code = AuthorizationCode.objects.get(
                code=code
            )

        except AuthorizationCode.DoesNotExist:
            return Response(
                {
                    "error": "Invalid authorization code."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # ✅ Expiry Validation 
        
        if authorization_code.expires_at < timezone.now():
            return Response(
                {
                    "error": "Authorization code has expired."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

         # ✅ Used Validation (ADD THIS HERE)
        if authorization_code.used:
            return Response(
                {
                    "error": "Authorization code has already been used."
                },
                status=status.HTTP_400_BAD_REQUEST,
            ) 

        print("🥬 Authorization Code Found:", authorization_code.code)
        print("👤 User:", authorization_code.user.email)
        
        tokens = generate_app_tokens(
            authorization_code.user
        )
        
        print("🎟️ Tokens Generated")
        
        authorization_code.used = True
        authorization_code.save()

        print("✅ Authorization Code Marked Used")
 
        response = Response(
            {
                "message": "Login successful."
            },
            status=status.HTTP_200_OK,
        )

        attach_auth_cookies(response, tokens)

        return response

class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        refresh_token = request.COOKIES.get(
            "capeark_refresh"
        )

        print("👻 Refresh Cookie:", refresh_token)

        if not refresh_token:
            return Response(
                {
                    "error": "Refresh cookie missing."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )       
        
        try:

            refresh = RefreshToken(refresh_token)

            print("👻 Refresh Token Valid")
            
            access_token = str(refresh.access_token)
            
            print("👻 New Access Token Generated")

        except TokenError:

            return Response(
                {
                    "error": "Invalid refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                "message": "Access token refreshed."
            },
            status=status.HTTP_200_OK,
        )
        
        response.set_cookie(
            "capeark_access",
            access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="None",
        )
        
        return response