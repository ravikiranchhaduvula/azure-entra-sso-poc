param(
    [string]$ResourceGroup,
    [string]$Location = "Australia East"
)

Write-Host ""
Write-Host "====================================="
Write-Host " Nexus Customer Portal Deployment"
Write-Host "====================================="
Write-Host ""

# Check Azure Login
$account = az account show --query name -o tsv 2>$null

if (-not $account) {
    Write-Host "You are not logged into Azure."
    az login
}

Write-Host ""
Write-Host "Current Subscription:"
az account show --output table

Write-Host ""

# Create Resource Group if it doesn't exist
az group create `
    --name $ResourceGroup `
    --location $Location

Write-Host ""
Write-Host "Deploying Bicep..."

az deployment group create `
    --resource-group $ResourceGroup `
    --template-file ../bicep/main.bicep `
    --parameters ../parameters/dev.bicepparam

Write-Host ""
Write-Host "Deployment completed."