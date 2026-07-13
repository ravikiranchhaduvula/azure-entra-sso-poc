# 00 - CapeArk Development Setup and Installation

## Status

✅ Completed

## Goal

Prepare a complete development environment for the CapeArk SSO learning
project.

## Technology Stack

-   Python 3.14
-   Django 6
-   Django REST Framework
-   SimpleJWT
-   SQLite (Development)
-   PostgreSQL (Other Environments)
-   Requests Library

## Packages Installed

``` bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install requests
```

## Project Setup

-   Created virtual environment
-   Created Django project (`config`)
-   Created `accounts` app
-   Added `rest_framework` and `accounts` to `INSTALLED_APPS`
-   Configured `AUTH_USER_MODEL`
-   Configured JWT authentication
-   Created `accounts/urls.py`
-   Registered URLs in `config/urls.py`
-   Created `auth_tokens.py`
-   Registered models in Django Admin

## Database

-   Reset SQLite database
-   Deleted migrations
-   Ran:

``` bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Development Workflow

Code → Test → Commit → Documentation

## Result

✅ Development environment ready.
