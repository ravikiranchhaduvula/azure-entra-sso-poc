# Nexus Customer Portal - Developer Provisioning Guide

## Overview

This document describes how to provision a Nexus Customer Portal into a customer Azure subscription.

The provisioning process is fully automated and consists of:

1. Deploy Infrastructure (Azure Bicep)
2. Retrieve Static Web App Deployment Token
3. Deploy Customer Portal using SWA CLI

---

# Architecture

```
Marketplace (Future)
        │
        ▼
Provisioning Service
        │
        ▼
deploy-infra.ps1
        │
        ├── Deploy Infrastructure (Bicep)
        │
        ├── Retrieve Deployment Token
        │
        └── Execute deploy-portal.ps1
                      │
                      ▼
                 SWA CLI Deploy
                      │
                      ▼
             Azure Static Web App
```

---

# Repository Structure

## Infrastructure Repository

```
nexus-customer-portal-infra
│
├── bicep
│   ├── main.bicep
│   └── staticwebapp.bicep
│
├── parameters
│   └── dev.bicepparam
│
├── scripts
│   ├── deploy-infra.ps1
│   └── deploy-portal.ps1
│
└── docs
```

---

## Customer Portal Repository

```
nexus-customer-portal
│
├── public
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── package.json
├── server.js
└── README.md
```

---

# Prerequisites

Install:

- Azure CLI
- Azure Bicep
- Azure Static Web Apps CLI (SWA CLI)
- Git
- PowerShell 7 (recommended)
- Node.js

---

# Verify Installation

```powershell
az version

az bicep version

swa --version

node -v

npm -v
```

---

# Azure Login

Login

```powershell
az login
```

Select Customer Subscription

```powershell
az account set --subscription "<Customer Subscription>"
```

Verify

```powershell
az account show --output table
```

---

# Resource Group

The Resource Group must be created in a region that supports Azure Static Web Apps.

Current POC region:

```
East Asia
```

Create Resource Group

```powershell
az group create `
    --name nexus-customer-portal-rg `
    --location eastasia
```

Verify

```powershell
az group show `
    --name nexus-customer-portal-rg `
    --query "{name:name,location:location}"
```

Expected

```json
{
    "name": "nexus-customer-portal-rg",
    "location": "eastasia"
}
```

---

# Provision Customer Portal

Navigate to:

```powershell
cd nexus-customer-portal-infra\scripts
```

Run

```powershell
.\deploy-infra.ps1 `
    -ResourceGroup "nexus-customer-portal-rg" `
    -StaticWebAppName "contoso-portal-dev" `
    -CustomerName "Contoso"
```

The provisioning script performs:

1. Deploy Azure Infrastructure
2. Create Static Web App
3. Retrieve Deployment Token
4. Deploy Customer Portal

No manual Deployment Token copy is required.

---

# Deployment Verification

Verify Static Web App

```powershell
az staticwebapp list --output table
```

Open

```
https://<static-web-app>.azurestaticapps.net
```

Expected

- Customer Portal loads
- CSS loads
- JavaScript loads
- Login page is displayed

---

# Manual Deployment Token Retrieval (Troubleshooting)

```powershell
az staticwebapp secrets list `
    --name contoso-portal-dev `
    --resource-group nexus-customer-portal-rg `
    --query "properties.apiKey" `
    -o tsv
```

---

# Manual Portal Deployment (Troubleshooting)

```powershell
swa deploy .\public `
    --deployment-token "<Deployment Token>"
```

---

# Current Provisioning Flow

```
Developer

↓

deploy-infra.ps1

↓

Deploy Azure Bicep

↓

Create Static Web App

↓

Retrieve Deployment Token

↓

deploy-portal.ps1

↓

SWA CLI

↓

Deploy Customer Portal

↓

Customer Portal Ready
```

---

# Future Production Flow

```
Azure Marketplace

↓

Provisioning Service

↓

Deploy Infrastructure

↓

Retrieve Deployment Token

↓

Deploy Customer Portal

↓

Register Portal

↓

Send Welcome Email

↓

Customer Login
```

---

# Future Enhancements

- Azure Marketplace Integration
- Customer Portal Registration
- Microsoft Entra ID Authentication
- Nexus Authentication Integration
- Automated Customer Onboarding
- Versioned Portal Package Deployment

---

# Current Status

## Infrastructure

- ✅ Azure Bicep
- ✅ Static Web App
- ✅ Automated Deployment

## Customer Portal

- ✅ Local Development
- ✅ Automated SWA Deployment

## Authentication

- ⬜ Microsoft Entra ID
- ⬜ Nexus Authentication
- ⬜ JWT Integration

## Marketplace

- ⬜ Automated Provisioning