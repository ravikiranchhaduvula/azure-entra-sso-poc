# TapeArk SSO Learning Notes

## Authentication Refactoring (Phase 1)

### Project Goal

Build a production-style authentication system that supports:

-   Email Registration
-   Email OTP Login
-   Microsoft Entra ID Login
-   JWT Authentication
-   Refresh Tokens
-   Protected APIs

The long-term objective is to have **one authentication system**
regardless of how users sign in.

------------------------------------------------------------------------

# Initial Problem

At the beginning of the project we created a custom model:

``` python
class AppUser(models.Model):
```

This model stored:

-   email
-   name
-   phone
-   auth_provider
-   Entra IDs

We also created:

-   LoginOtp
-   Registration
-   OTP Login
-   JWT generation

Everything was built around `AppUser`.

However Django itself was still using its own authentication model:

``` python
django.contrib.auth.models.User
```

because we never configured:

``` python
AUTH_USER_MODEL
```

------------------------------------------------------------------------

# Why this became a problem

The project accidentally had **two user models**.

``` text
AppUser
│
├── Registration
├── OTP
├── LoginOtp
├── JWT Claims
└── Entra

------------------------------

Django User
│
├── request.user
├── Django Admin
├── JWT Authentication
└── Permissions
```

This caused confusing runtime errors.

Examples:

-   `request.user` returned Django User.
-   OTP returned `AppUser`.
-   JWT expected `AppUser`.
-   Dashboard authenticated Django User.

Different parts of the application were working with different user
objects.

------------------------------------------------------------------------

# Decision

Instead of trying to patch two user models together, we decided to make
**AppUser** the single source of truth.

This is the same approach used in most enterprise Django applications.

------------------------------------------------------------------------

# Database Reset

Because this was still a learning project using SQLite, we chose to
reset the development database.

Deleted:

-   `db.sqlite3`
-   `accounts/migrations/*` (kept `__init__.py`)

Reason:

Django recommends defining a custom authentication model **before the
first migration**.

Resetting now is much cleaner than migrating later.

------------------------------------------------------------------------

# AppUser Refactor

Old:

``` python
class AppUser(models.Model)
```

New:

``` python
class AppUser(AbstractUser)
```

Reason:

`AbstractUser` already provides:

-   username
-   password
-   email
-   first_name
-   last_name
-   last_login
-   date_joined
-   permissions
-   groups
-   staff support

Instead of rebuilding authentication ourselves, we extend Django's
implementation.

This is considered Django best practice.

------------------------------------------------------------------------

# AUTH_USER_MODEL

Added to:

`config/settings.py`

``` python
AUTH_USER_MODEL = "accounts.AppUser"
```

Reason:

This tells Django that every authentication operation should use
`AppUser` instead of the built-in `User` model.

From this point onward:

``` python
request.user
```

returns:

``` text
AppUser
```

instead of:

``` text
django.contrib.auth.models.User
```

------------------------------------------------------------------------

# Email Authentication

Configured inside `AppUser`:

``` python
USERNAME_FIELD = "email"
REQUIRED_FIELDS = ["username"]
```

Reason:

Enterprise systems usually authenticate users by email.

Examples:

-   Microsoft Entra
-   Google
-   Okta
-   Auth0

This aligns Django authentication with enterprise identity providers.

------------------------------------------------------------------------

# Email Normalization

Added:

``` python
def save(...)
```

to automatically convert:

``` text
Ravi@Example.Com
```

into:

``` text
ravi@example.com
```

Reason:

Email addresses should be stored consistently.

This avoids duplicate accounts caused by different capitalization.

------------------------------------------------------------------------

# Name Property

Instead of creating another database column called `name`, we added:

``` python
@property
def name(self):
```

Reason:

The database stores:

-   `first_name`
-   `last_name`

The property simply combines them.

Benefits:

-   avoids duplicated data
-   keeps code readable

Example:

``` python
user.name
```

still works.

------------------------------------------------------------------------

# Auth Provider

Kept:

``` python
auth_provider
```

Values:

-   `NORMAL`
-   `ENTRA`

Reason:

The application needs to know how a user originally authenticated.

Future providers could include:

-   GOOGLE
-   GITHUB
-   OKTA

------------------------------------------------------------------------

# Microsoft Entra Fields

Kept:

-   `entra_object_id`
-   `entra_tenant_id`

Reason:

These uniquely identify a Microsoft identity.

Useful later for:

-   multi-tenant authentication
-   synchronization
-   audit logging

------------------------------------------------------------------------

# LoginOtp

No structural changes.

Reason:

OTP belongs to a specific `AppUser`.

Relationship:

``` text
AppUser
   1
   │
   ▼
LoginOtp
 Many
```

------------------------------------------------------------------------

# Django Admin

Previously:

``` python
ModelAdmin
```

Now:

``` python
UserAdmin
```

Reason:

`UserAdmin` automatically supports:

-   passwords
-   permissions
-   groups
-   staff
-   superuser
-   last login
-   date joined

We only added our enterprise-specific fields.

------------------------------------------------------------------------

# Migrations

Executed:

``` bash
python manage.py makemigrations
python manage.py migrate
```

Successfully created:

-   AppUser
-   LoginOtp

Database recreated successfully.

------------------------------------------------------------------------

# Current Architecture

``` text
                 Microsoft Entra
                       │
                       ▼
                  AppUser
                     ▲
                     │
             Registration
                     ▲
                     │
                OTP Login
                     │
                     ▼
             JWT Authentication
                     │
                     ▼
               request.user
```

Every authentication flow now points to a single user model.

------------------------------------------------------------------------

# Why This Architecture

Using one user model provides several benefits:

-   No duplicate user information.
-   Consistent authentication across all login methods.
-   Simpler JWT generation and validation.
-   Easier integration with Django Admin and permissions.
-   Cleaner foundation for enterprise identity providers such as
    Microsoft Entra.

------------------------------------------------------------------------

# Current Status

-   ✅ Custom authentication model completed
-   ✅ Django configured to use AppUser
-   ✅ Database recreated
-   ✅ Admin working
-   ✅ Foundation ready

------------------------------------------------------------------------

# Next Phase

The next milestone (not yet implemented) is to rebuild the
authentication flow on top of this new foundation:

1.  Registration API
2.  OTP Login
3.  JWT Access Token
4.  Refresh Token
5.  Protected Dashboard
6.  Microsoft Entra Login

These will all use the same `AppUser` model.
