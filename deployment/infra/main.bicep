param location string = resourceGroup().location
param environmentName string = 'csu-graphql'
param containerRegistryName string = 'graphqlacr'
param deployApim bool = true
param apimName string = 'graph-api-mgmt-${uniqueString(resourceGroup().id)}'

module apim 'apim.bicep' = if (deployApim) {
  name: '${deployment().name}--apim'
  params: {
    apimName: apimName
    publisherName: 'Graphql Store'
    publisherEmail: 'demo@example.com'
    apimLocation: location
  }
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-12-01-preview' = {
  name: '${containerRegistryName}${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// // container app environment
module environment 'container_apps_env.bicep' = {
  name: 'container-app-environment'
  params: {
    environmentName: environmentName
    location: location
  }
}

output containerRegistryName string = containerRegistry.name
