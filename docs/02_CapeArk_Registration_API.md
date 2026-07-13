# 02_CapeArk_Registration_API

## Status

🚧 In Progress

------------------------------------------------------------------------

# Goal

Implement a production-style Registration API using Django's
authentication framework and the custom `AppUser` model.

The Registration API will create a new user that can later authenticate
using:

-   Email + Password
-   Email + OTP
-   Microsoft Entra ID

------------------------------------------------------------------------

# Why Registration?

The registration endpoint is the entry point into the authentication
system.

``` text
Client
   │
POST /api/register
   │
Serializer Validation
   │
AppUser.create_user()
   │
set_password()
   │
Database
```

------------------------------------------------------------------------

# Design Decisions

## Why ModelSerializer?

We chose `ModelSerializer` because:

-   It understands the `AppUser` model automatically.
-   Less boilerplate code.
-   Easier maintenance.
-   Standard Django REST Framework approach.

------------------------------------------------------------------------

## Why create_user()?

Instead of:

``` python
AppUser.objects.create(...)
```

we use:

``` python
AppUser.objects.create_user(...)
```

Reason:

-   Uses Django's authentication workflow.
-   Prepares the object as an authenticatable user.
-   Follows Django best practices.

------------------------------------------------------------------------

## Why keep set_password()?

Although `create_user()` can hash passwords automatically, we
intentionally keep:

``` python
password = validated_data.pop("password")

user = AppUser.objects.create_user(
    **validated_data
)

user.set_password(password)
user.save()
```

### Reason

This project is educational.

Keeping `set_password()` explicitly helps understand:

-   where password hashing occurs
-   how password reset works
-   how password change works
-   why raw passwords are never stored

This makes the authentication flow easier to understand later.

------------------------------------------------------------------------

## Why write_only=True?

``` python
password = serializers.CharField(
    write_only=True
)
```

Reason:

The client can send the password.

The API should NEVER return it.

------------------------------------------------------------------------

## Why validate email?

Registration should reject duplicate accounts.

Validation ensures one account per email address.

------------------------------------------------------------------------

# Files Modified

-   accounts/serializers.py

(Registration View, URL and testing will be documented after
implementation.)

------------------------------------------------------------------------

# Questions & Answers

### Q1. Why ModelSerializer instead of Serializer?

Because we are creating an AppUser model object. ModelSerializer
automatically maps model fields to serializer fields.

------------------------------------------------------------------------

### Q2. Why not use AppUser.objects.create()?

It bypasses Django's authentication workflow and is not the recommended
way to create authenticatable users.

------------------------------------------------------------------------

### Q3. Why keep set_password() if create_user() already hashes passwords?

For learning purposes.

It clearly demonstrates where hashing happens and prepares us for future
topics such as password reset and change password.

------------------------------------------------------------------------

### Q4. Why is password write_only?

To ensure the password is accepted in requests but never returned in API
responses.

------------------------------------------------------------------------

### Q5. Why validate duplicate emails?

To prevent multiple accounts using the same email address.

------------------------------------------------------------------------

# Current Progress

✅ Authentication Foundation completed

🚧 Registration Serializer in progress

⏳ Registration View

⏳ Registration Endpoint Testing

------------------------------------------------------------------------

# Next Phase

Complete:

-   RegisterSerializer
-   RegisterView
-   Register URL
-   Postman testing
-   Git commit

Then document the completed implementation.
