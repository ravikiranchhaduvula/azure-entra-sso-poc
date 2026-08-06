param(
    [Parameter(Mandatory)]
    [string]$ResourceGroup,

    [Parameter(Mandatory)]
    [string]$StaticWebAppName,

    [Parameter(Mandatory)]
    [string]$CustomerName,

    [string]$Environment = "dev",

    [string]$Location = "Australia East",

    [Parameter(Mandatory)]
    [string]$PortalPath
)

Write-Host ""
Write-Host "=========================================="
Write-Host " Nexus Customer Portal Provisioning"
Write-Host "=========================================="
Write-Host ""

# Check Azure Login
$account = az account show --query name -o tsv 2>$null

if (-not $account) {
    Write-Host "Not logged into Azure. Launching login..."
    az login
}

Write-Host ""
Write-Host "Deploying infrastructure..."
Write-Host ""

az deployment group create `
    --resource-group $ResourceGroup `
    --template-file ../bicep/main.bicep `
    --parameters `
        staticWebAppName=$StaticWebAppName `
        customerName=$CustomerName `
        environment=$Environment

if ($LASTEXITCODE -ne 0) {
    throw "Infrastructure deployment failed."
}

Write-Host ""
Write-Host "Retrieving deployment token..."
Write-Host ""

$deploymentToken = az staticwebapp secrets list `
    --name $StaticWebAppName `
    --resource-group $ResourceGroup `
    --query "properties.apiKey" `
    -o tsv

if ([string]::IsNullOrWhiteSpace($deploymentToken)) {
    throw "Unable to retrieve deployment token."
}

Write-Host "Deployment token retrieved successfully."

Write-Host ""
Write-Host "Deploying customer portal..."
Write-Host ""

.\deploy-portal.ps1 `
    -PortalPath $PortalPath `
    -DeploymentToken $deploymentToken

# Remove token from memory
$deploymentToken = $null

Write-Host ""
Write-Host "=========================================="
Write-Host " Provisioning completed successfully"
Write-Host "=========================================="