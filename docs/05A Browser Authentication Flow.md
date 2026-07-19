# 05A - Browser Authentication Flow (Completed)

## Objective

Build a browser-based authentication flow on top of the Django REST
APIs.

The browser should:

-   Login using Email + Password
-   Receive OTP challenge
-   Verify OTP
-   Receive JWT tokens
-   Store tokens in Browser Session Storage
-   Access protected Dashboard API
-   Logout

------------------------------------------------------------------------

## High Level Architecture

``` text
Browser (HTML + JavaScript)
        |
        v
Django REST APIs
        |
        v
SQLite Database
```

## Browser Pages

-   `/` → Login Page
-   `/otp-page/` → OTP Verification Page
-   `/dashboard-page/` → Dashboard

## REST APIs

-   POST `api/auth/register/`
-   POST `api/auth/login/`
-   POST `api/auth/verify-otp/`
-   GET `api/auth/dashboard/`
-   POST `api/auth/token/refresh/`

## Authentication Flow

``` text
Login
  ↓
Email + Password
  ↓
POST /login/
  ↓
Generate OTP
  ↓
OTP Page
  ↓
POST api/auth/verify-otp/
  ↓
JWT Tokens
  ↓
Store in sessionStorage
  ↓
Dashboard
  ↓
GET api/auth/dashboard/
```

## Frontend Structure

    frontend/
    ├── templates/
    │   ├── login.html
    │   ├── otp.html
    │   └── dashboard.html
    ├── static/
    │   ├── css/styles.css
    │   └── js/app.js
    ├── views.py
    └── urls.py

## Session Storage

After OTP verification:

-   Access Token
-   Refresh Token
-   User Information

Stored using:

``` javascript
sessionStorage.setItem(...)
```

## Dashboard

Uses the stored Access Token to call:

`GET /api/auth/dashboard/`

Header:

`Authorization: Bearer <Access Token>`

Displays:

-   Name
-   Email
-   Username
-   Authentication Provider

## Logout

-   Clear Session Storage
-   Redirect to Login Page

## Completed

-   Registration
-   Password Hashing
-   Login
-   OTP Authentication
-   JWT Generation
-   Refresh Token
-   Browser Login
-   Browser OTP Page
-   Browser Dashboard
-   Protected Dashboard API
-   Session Storage
-   Logout

## Next Phase

Mock Microsoft Entra ID Integration followed by Real Microsoft Entra ID.
