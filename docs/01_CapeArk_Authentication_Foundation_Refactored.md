# 01 - CapeArk Authentication Foundation

## Status

✅ Completed

## Goal

Establish a single authentication model using Django's AbstractUser.

## Key Decisions

-   Replaced custom `models.Model` user with `AbstractUser`
-   Configured `AUTH_USER_MODEL`
-   Email used as login (`USERNAME_FIELD = "email"`)
-   Added enterprise fields:
    -   phone
    -   auth_provider
    -   entra_object_id
    -   entra_tenant_id

## Inherited Django Features

-   password
-   last_login
-   date_joined
-   is_active
-   is_staff
-   is_superuser
-   groups
-   permissions

## Files Modified

-   accounts/models.py
-   accounts/admin.py
-   config/settings.py

## Lessons Learned

One authentication model is simpler, safer and aligns with Django best
practices.

## Result

✅ Authentication foundation completed.
