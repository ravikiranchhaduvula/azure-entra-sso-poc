# CapeArk Authentication Service

## Phase 6 – Dockerization & Azure Deployment Guide

This guide consolidates the Dockerization and Azure App Service deployment steps.

### Architecture

```text
Local Development
      │
      ▼
Docker Image
      │
      ▼
Azure Container Registry
      │
      ▼
Azure App Service
      │
      ▼
Login → OTP → JWT → Dashboard
```

## Phase 6.1

1. Generate requirements.txt using `python -m pip freeze > requirements.txt`.
2. Create `Dockerfile`.
3. Create `.dockerignore` excluding `.venv`, `.git`, `db.sqlite3`, etc.
4. Build image:
```powershell
docker build -t capeark-sso .
```
5. Run image:
```powershell
docker run --rm -p 8000:8000 capeark-sso
```
6. Create `seed_demo_user` management command and start container with:
```text
migrate -> seed_demo_user -> runserver
```

## Phase 6.2

### Azure Resources
- Resource Group: `capeark-auth-rg`
- Customer RG: `customer-portal-rg`
- App Service Plan: `capeark-auth-plan`
- ACR: `capearkauthacr2026`
- Web App: `capeark-auth-ravi-2026`

### Azure CLI
```powershell
az login --use-device-code
az group create --name capeark-auth-rg --location australiaeast
az appservice plan create --name capeark-auth-plan --resource-group capeark-auth-rg --is-linux --sku B1
az acr create --resource-group capeark-auth-rg --name capearkauthacr2026 --sku Basic
az acr login --name capearkauthacr2026
```

### Push Docker Image
```powershell
docker tag capeark-sso capearkauthacr2026.azurecr.io/capeark-sso:v1
docker push capearkauthacr2026.azurecr.io/capeark-sso:v1
```

### Create Web App
```powershell
az webapp create --resource-group capeark-auth-rg --plan capeark-auth-plan --name capeark-auth-ravi-2026 --deployment-container-image-name capearkauthacr2026.azurecr.io/capeark-sso:v1
```

### Configure Managed Identity + AcrPull
Assign identity, grant AcrPull, enable `acrUseManagedIdentityCreds`, configure container, set `WEBSITES_PORT=8000`, restart, tail logs.

### Updating Images
Build v2, push, update container configuration, restart.

### Common Issue
If `DisallowedHost` occurs, add Azure hostname to `ALLOWED_HOSTS`, rebuild, push, restart.

## Outcome
- Dockerized Django
- Azure App Service
- Azure Container Registry
- Automatic migrations
- Demo user creation
- OTP + JWT authentication running in Azure.
