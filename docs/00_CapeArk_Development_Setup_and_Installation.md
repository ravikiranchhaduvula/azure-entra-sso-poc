# Phase 01 - Authentication Foundation

**Project:** CapeArk SSO Learning Project

**Status:** ✅ Completed

**Prerequisites:**
- 00_Development_Setup_and_Installation.md

**Estimated Time:** 2–3 hours

**Difficulty:** Intermediate

**Last Updated:** 2026-07-12


# CapeArk SSO Development Environment & Installation Guide

## Purpose

This document captures the environment setup and commands used while
building the CapeArk SSO learning project. It is intended to make it
easy to recreate the project from scratch.

------------------------------------------------------------------------

# Technology Stack

-   Python 3.14
-   Django 6.x
-   Django REST Framework
-   Simple JWT
-   SQLite (Development)
-   PostgreSQL (Other environments)
-   Microsoft Entra ID (Mock first, real integration later)

------------------------------------------------------------------------

# Create Project

``` bash
python -m venv .venv
```

Activate

### Windows PowerShell

``` powershell
.\.venv\Scripts\Activate.ps1
```

------------------------------------------------------------------------

# Install Core Packages

``` bash
pip install django
```

``` bash
pip install djangorestframework
```

``` bash
pip install djangorestframework-simplejwt
```

``` bash
pip install requests
```

## Why requests?

Used by the Entra callback to exchange the authorization code for tokens
with the identity provider (mock server now, Microsoft Entra later).

------------------------------------------------------------------------

# Create Django Project

``` bash
django-admin startproject config .
```

Create application

``` bash
python manage.py startapp accounts
```

------------------------------------------------------------------------

# Register Applications

Add to `INSTALLED_APPS`:

-   rest_framework
-   accounts

------------------------------------------------------------------------

# Configure Custom User Model

In `config/settings.py`

``` python
AUTH_USER_MODEL = "accounts.AppUser"
```

------------------------------------------------------------------------

# Configure JWT

``` python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
```

``` python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

------------------------------------------------------------------------

# Development Database Reset

Development only:

-   Delete `db.sqlite3`
-   Delete all files inside `accounts/migrations/` except `__init__.py`

Reason: Introduce the custom authentication model before the first
migration.

------------------------------------------------------------------------

# Create Database

``` bash
python manage.py makemigrations
```

``` bash
python manage.py migrate
```

------------------------------------------------------------------------

# Create Administrator

``` bash
python manage.py createsuperuser
```

------------------------------------------------------------------------

# Run Development Server

``` bash
python manage.py runserver
```

Open:

-   http://localhost:8000/admin/

------------------------------------------------------------------------

# Development Workflow

1.  Modify models
2.  Run `makemigrations`
3.  Run `migrate`
4.  Start server
5.  Test with Postman/browser
6.  Commit to Git

------------------------------------------------------------------------

# Documentation Strategy

Each completed implementation gets its own document.

Current documents:

-   `01_Authentication_Foundation.md`

Upcoming documents:

-   `02_Registration_API.md`
-   `03_Email_OTP_Login.md`
-   `04_JWT_Access_Refresh.md`
-   `05_Protected_APIs.md`
-   `06_Django_Admin.md`
-   `07_Microsoft_Entra_Login.md`
-   `08_RBAC_Permissions.md`
-   `09_Multi_Tenant_Authentication.md`

This keeps the repository modular, easy to navigate, and similar to
enterprise engineering documentation.
