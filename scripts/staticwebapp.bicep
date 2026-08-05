@description('Azure region')
param location string

@description('Static Web App name')
param staticWebAppName string

@description('Resource tags')
param tags object

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: staticWebAppName
  location: location

  tags: tags

  sku: {
    name: 'Free'
    tier: 'Free'
  }

  properties: {}
}

output staticWebAppId string = staticWebApp.id
output staticWebAppName string = staticWebApp.name
output defaultHostname string = staticWebApp.properties.defaultHostname