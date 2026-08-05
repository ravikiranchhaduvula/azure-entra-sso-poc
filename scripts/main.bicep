targetScope = 'resourceGroup'

@description('Azure region')
param location string = resourceGroup().location

@description('Static Web App name')
param staticWebAppName string

@description('Environment')
param environment string = 'dev'

var tags = {
  Application: 'Nexus Customer Portal'
  Environment: environment
  ManagedBy: 'Bicep'
}

module staticWebApp './staticwebapp.bicep' = {
  name: 'customerPortal'
  params: {
    location: location
    staticWebAppName: staticWebAppName
    tags: tags
  }
}

output staticWebAppId string = staticWebApp.outputs.staticWebAppId
output staticWebAppName string = staticWebApp.outputs.staticWebAppName
output defaultHostname string = staticWebApp.outputs.defaultHostname