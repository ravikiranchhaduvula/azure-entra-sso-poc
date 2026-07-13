# 05_CapeArk_Protected_APIs

## Status

✅ Completed

## Goal

Protect APIs by default and expose only authentication endpoints
publicly.

## Files Modified

-   config/settings.py
-   accounts/views.py

## Summary

-   Enabled global JWT authentication.
-   Enabled global `IsAuthenticated`.
-   Added `AllowAny` to Register, Login, Verify OTP, Entra Start and
    Entra Callback.
-   Dashboard remains protected.

## Testing

-   Register ✅
-   Login ✅
-   Verify OTP ✅
-   Dashboard without token → 401 ✅
-   Dashboard with token → 200 ✅

## Lessons Learned

Secure-by-default is the preferred enterprise security model.

## Next Phase

06_CapeArk_Django_Admin_and_User_Management
