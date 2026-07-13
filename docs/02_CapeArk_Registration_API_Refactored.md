# 02 - CapeArk Registration API

## Status

✅ Completed

## Goal

Create users securely using the custom AppUser model.

## Files Modified

-   accounts/serializers.py
-   accounts/views.py
-   accounts/urls.py

## Implementation

-   ModelSerializer
-   Email validation
-   create_user()
-   set_password()
-   RegisterView
-   Registration endpoint

## Testing

-   Registration successful
-   Duplicate email validation
-   Password stored as PBKDF2 hash
-   User verified in Django Admin

## Lessons Learned

Never store plain-text passwords. Always use `set_password()`.

## Result

✅ Registration completed.
