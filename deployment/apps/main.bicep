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
  // payments: {
  //   appName: 'payments'
  //   containerImage: '${containerRegistryName}${uniqueString(resourceGroup().id)}.azurecr.io/payments:latest'
  //   containerPort: 8800
  //   env: [
  //     {
  //       name: 'PORT_NUMBER'
  //       value: 'Application running on port 8800'
  //     }
  //   ]
  // }
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