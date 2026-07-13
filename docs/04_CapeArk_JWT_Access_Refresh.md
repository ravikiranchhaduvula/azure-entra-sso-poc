# 04_CapeArk_JWT_Access_Refresh

## Status

✅ Completed

## Goal

Understand and validate JWT Access and Refresh token generation.

## Files Modified

-   accounts/auth_tokens.py

## Implementation

``` python
from rest_framework_simplejwt.tokens import RefreshToken

def generate_app_tokens(user):
    refresh = RefreshToken.for_user(user)
    refresh["email"] = user.email
    refresh["username"] = user.username
    refresh["auth_provider"] = user.auth_provider
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
```

## Testing

-   JWT decoded successfully
-   Access token validated
-   Refresh token validated
-   Dashboard authenticated
-   Custom claims verified

## Lessons Learned

-   `RefreshToken.for_user()` creates the JWT pair.
-   Custom claims flow into the Access Token.
-   Never store sensitive information in JWT claims.

## Next Phase

05_CapeArk_Protected_APIs
