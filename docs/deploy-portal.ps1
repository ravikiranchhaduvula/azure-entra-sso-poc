param(
    [Parameter(Mandatory)]
    [string]$PortalPath,

    [Parameter(Mandatory)]
    [string]$DeploymentToken
)

Write-Host ""
Write-Host "=========================================="
Write-Host " Deploying Nexus Customer Portal"
Write-Host "=========================================="
Write-Host ""

swa deploy $PortalPath `
    --deployment-token $DeploymentToken

if ($LASTEXITCODE -ne 0) {
    throw "Customer Portal deployment failed."
}

Write-Host ""
Write-Host "Customer Portal deployed successfully."
Write-Host ""