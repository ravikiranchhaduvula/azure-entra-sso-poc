# Nexus Customer Portal Infrastructure

## Overview

This repository contains the Infrastructure as Code (IaC) required to deploy the Nexus Customer Portal into a customer's Azure subscription using Azure Bicep.

The infrastructure is intentionally separated from the application source code to follow enterprise deployment practices.

This repository currently deploys:

- Azure Static Web App

Future enhancements may include:

- Azure Key Vault
- Application Insights
- Storage Account
- Log Analytics
- Azure Monitor
- Other customer-specific infrastructure

---

# Architecture

```
Azure Marketplace (Future)
           │
           ▼
Provisioning Service
           │
           ▼
Azure Bicep Templates
           │
           ▼
Customer Azure Subscription
           │
           ▼
Azure Static Web App
           │
           ▼
Customer Portal
```

For the current Proof of Concept (POC), deployments are executed manually using Azure CLI. In production, Azure Marketplace (or an equivalent provisioning service) will trigger the same deployment process.

---

# Repository Structure

```
nexus-customer-portal-infra
│
├── bicep
│   ├── main.bicep
│   └── staticwebapp.bicep
│
├── parameters
│   ├── dev.bicepparam
│   └── prod.bicepparam (future)
│
├── scripts
│   └── deploy.ps1
│
└── docs
```

---

# Deployment Scope

This infrastructure is deployed into the **customer's Azure subscription**.

Vendor-hosted services such as:

- CapeArk Authentication
- Nexus APIs
- Shared Services

remain deployed within the vendor subscription.

Each customer receives an independent Azure Static Web App deployed into their own Azure subscription.

---

# Deployment

Login to Azure

```bash
az login
```

Select the customer subscription

```bash
az account set --subscription "<Customer Subscription Name or ID>"
```

Create a Resource Group (if required)

```bash
az group create \
    --name nexus-customer-portal-rg \
    --location australiaeast
```

Deploy the infrastructure

```bash
az deployment group create \
    --resource-group nexus-customer-portal-rg \
    --template-file bicep/main.bicep \
    --parameters \
        staticWebAppName=contoso-portal-dev \
        customerName=Contoso \
        environment=dev
```

---

# Current Resources

Current deployment creates:

- Azure Static Web App

---

# Future Roadmap

The following enhancements are planned:

- Azure Marketplace integration
- Automated customer provisioning
- Customer Portal registration
- GitHub repository integration
- Microsoft Entra authentication
- Dynamic trusted portal registration
- Customer onboarding automation

---

# Design Principles

- Infrastructure and application code are maintained in separate repositories.
- Infrastructure templates remain reusable and environment-independent.
- Business logic is not embedded within Bicep templates.
- Customer-specific values are supplied during deployment.
- Infrastructure is deployed into customer-owned Azure subscriptions.

---