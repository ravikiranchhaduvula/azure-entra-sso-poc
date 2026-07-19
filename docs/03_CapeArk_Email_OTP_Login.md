# 03_CapeArk_Email_OTP_Login

## Status

✅ Completed

## Goal

Implement Email + Password + OTP authentication followed by JWT Access
and Refresh Tokens.

## Authentication Flow

``` text
Email + Password
        │
 authenticate()
        │
 Generate OTP
        │
 Save LoginOtp
        │
 Verify OTP
        │
 Update last_login
        │
 Generate JWT Tokens
        │
 Access Protected APIs
```

## Files Modified

-   accounts/serializers.py
-   accounts/views.py
-   accounts/auth_tokens.py

## Design Decisions

### Why authenticate()?

Uses Django's authentication backend to safely validate the user's
password.

### Why LoginOtp?

Keeps OTPs independent from the user record, allowing expiry and
one-time usage.

### Why verified?

Prevents reuse of an OTP after successful login.

### Why expires_at?

Limits OTP validity to reduce replay attacks.

### Why last_login?

Records the most recent successful authentication. This field is
inherited from AbstractUser.

### Why issue JWT after OTP?

JWT tokens are only created after both authentication factors succeed.

## APIs

### POST api/auth/login/

Authenticates email and password, generates an OTP and stores it.

### POST /api/auth/verify-otp/

Validates the OTP, marks it verified, updates last_login and returns JWT
Access and Refresh Tokens.

### GET /api/auth/dashboard/

Protected endpoint that requires a valid Access Token.

### POST /api/auth/token/refresh/

Uses a valid Refresh Token to issue a new Access Token.

## Testing Completed

-   Login API
-   Password authentication
-   OTP generation
-   LoginOtp record creation
-   OTP verification
-   verified flag update
-   last_login update
-   JWT Access Token
-   JWT Refresh Token
-   Dashboard endpoint
-   Refresh endpoint

All tests passed successfully.

## Common Mistakes

-   Using AppUser.objects.get() instead of authenticate()
-   Returning JWT before OTP verification
-   Forgetting to update last_login
-   Forgetting to mark OTP as verified
-   Accepting expired OTPs

## Interview Questions

**Why use authenticate()?** Because Django safely validates hashed
passwords using the configured authentication backend.

**Why generate JWT after OTP?** Authentication should be fully completed
before issuing tokens.

**Why separate LoginOtp from AppUser?** OTPs have their own lifecycle
and expiry.

**Why use Refresh Tokens?** To issue new Access Tokens without requiring
another login.

## Lessons Learned

-   authenticate() should be used for password verification.
-   OTP acts as a second authentication factor.
-   JWT should only be generated after complete authentication.
-   Refresh Tokens improve usability while maintaining security.

## Completion Checklist

-   [x] LoginSerializer
-   [x] LoginView
-   [x] VerifyOtpSerializer
-   [x] VerifyOtpView
-   [x] JWT Generation
-   [x] Protected Dashboard
-   [x] Refresh Token
-   [x] End-to-End Testing

## Phase Result

🎉 Phase 03 -- CapeArk Email OTP Login completed successfully.

## Next Phase

**04_CapeArk_JWT_Access_Refresh**
