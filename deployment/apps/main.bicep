param location string = resourceGroup().location
param environmentName string = 'csu-graphql'
param containerRegistryName string = 'graphqlacr'
param deployApim bool = true
param apimName string = 'graph-api-mgmt-${uniqueString(resourceGroup().id)}'

param containerAppsObjects object = {
  accounts: {
    appName: 'accounts'
    containerImage: '${containerRegistryName}${uniqueString(resourceGroup().id)}.azurecr.io/accounts:latest'
    containerPort: 8000
    env: [
      {
        name: 'PORT_NUMBER'
        value: 'Application running on port 8000'
      }
    ]
  }
  payments: {
    appName: 'payments'
    containerImage: '${containerRegistryName}${uniqueString(resourceGroup().id)}.azurecr.io/payments:latest'
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
      name: 'ACCOUNTS_ENDPOINT'
      value: '${containerApps[0].outputs.fqdn}/graphql'
    }
    {
      name: 'PAYMENTS_ENDPOINT'
      value: '${containerApps[1].outputs.fqdn}/graphql'

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

resource apimInstance 'Microsoft.ApiManagement/service@2020-12-01' existing = {
  name: apimName
}

resource petshopApi 'Microsoft.ApiManagement/service/apis@2020-12-01' = {
  name: 'bank'
  parent: apimInstance
  properties: {
    path: '/bank'
    apiRevision: '1'
    displayName: 'Bank API'
    description: 'Bank API'
    apiType: 'graphql'
    subscriptionRequired: true
    serviceUrl: gatewayApp.outputs.fqdn
    subscriptionKeyParameterNames: {
      header: 'api-key'
      query: 'api-key'
    }
    protocols: [
      'https'
    ]
  }
}
