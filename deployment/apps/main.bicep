param location string = resourceGroup().location
param environmentName string = 'csu-graphql'
param containerRegistryName string = 'graphqlacr'
param deployApim bool = true
param apimName string = 'graph-api-mgmt-${uniqueString(resourceGroup().id)}'

param containerAppsObjects object = {
  founders: {
    appName: 'founders'
    containerImage: '${containerRegistryName}${uniqueString(resourceGroup().id)}.azurecr.io/founders:latest'
    containerPort: 8000
    env: [
      {
        name: 'PORT_NUMBER'
        value: 'Application running on port 8000'
      }
    ]
  }
  companies: {
    appName: 'companies'
    containerImage: '${containerRegistryName}${uniqueString(resourceGroup().id)}.azurecr.io/companies:latest'
    containerPort: 8800
    env: [
      {
        name: 'PORT_NUMBER'
        value: 'Application running on port 8800'
      }
    ]
  }
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-12-01-preview' existing = {
  name: '${containerRegistryName}${uniqueString(resourceGroup().id)}'
}

module containerApps 'container_apps.bicep' = [for app in items(containerAppsObjects): {
  name: app.value.appName
  params: {
    location: location
    containerAppName: app.value.appName
    environmentName: environmentName
    containerImage: app.value.containerImage
    containerPort: app.value.containerPort

    env: app.value.env
    containerRegistryName: containerRegistry.name
    containerLoginServer: containerRegistry.properties.loginServer
    containerRegistryPassword: containerRegistry.listCredentials().passwords[0].value

  }
}]

var gatewayContainerApp = {
  appName: 'gateway'
  containerImage: '${containerRegistryName}${uniqueString(resourceGroup().id)}.azurecr.io/gateway:latest'
  containerPort: 7000
  env: [
    {
      name: 'FOUNDERS_ENDPOINT'
      value: 'https://${containerApps[0].outputs.fqdn}/graphql'
    }
    {
      name: 'COMPANIES_ENDPOINT'
      value: 'https://${containerApps[1].outputs.fqdn}/graphql'

    }
  ]
}

module gatewayApp 'container_apps.bicep' = {
  name: 'gateway'
  params: {
    location: location
    containerAppName: gatewayContainerApp.appName
    environmentName: environmentName
    containerImage: gatewayContainerApp.containerImage
    containerPort: gatewayContainerApp.containerPort

    env: gatewayContainerApp.env
    containerRegistryName: containerRegistry.name
    containerLoginServer: containerRegistry.properties.loginServer
    containerRegistryPassword: containerRegistry.listCredentials().passwords[0].value

  }
}

resource apimInstance 'Microsoft.ApiManagement/service@2021-04-01-preview' existing = {
  name: apimName
}

resource gatewayApiAPIM 'Microsoft.ApiManagement/service/apis@2021-04-01-preview' = {
  name: 'microcrunch'
  parent: apimInstance
  properties: {
    path: '/microcrunch'
    apiRevision: '1'
    displayName: 'MicroCrunch'
    description: 'MicroCrunch API'
    apiType: 'graphql'
    type: 'graphql'
    subscriptionRequired: true
    format: 'graphql-link'
    serviceUrl: 'https://${gatewayApp.outputs.fqdn}/graphql'
    protocols: [
      'https'
    ]
  }
}

// resource bankAPISchema 'Microsoft.ApiManagement/service/apis/schemas@2021-12-01-preview' = {
//   name: 'graphql'
//   parent: bankAPI
//   properties: {
//     contentType: 'application/vnd.ms-azure-apim.graphql.schema'
//     document: {
//       value: loadTextContent('../../schema.graphql')
//     }
//   }
// }

output graphqlEndpoint string = 'https://${gatewayApp.outputs.fqdn}'
output apiId string = gatewayApiAPIM.name
output apimName string = apimInstance.name
