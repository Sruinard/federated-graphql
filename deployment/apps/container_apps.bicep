param containerAppName string
param location string
param environmentName string

param containerImage string
param containerPort int

param isPrivateRegistry bool = true
param containerRegistryName string
param containerLoginServer string
param containerRegistryPassword string

// to find the role definition id, use: https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
param isExternalIngress bool = true
param enableIngress bool = true
param minReplicas int = 0
param env array = []
var cpu = json('1.5')
var memory = '3Gi'

resource environment 'Microsoft.App/managedEnvironments@2022-01-01-preview' existing = {
  name: environmentName
}

resource containerApp 'Microsoft.App/containerApps@2022-01-01-preview' = {
  name: containerAppName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: environment.id
    configuration: {
      secrets: [
        {
          name: 'container-registry-password'
          value: containerRegistryPassword
        }
      ]
      registries: isPrivateRegistry ? [
        {
          server: containerLoginServer
          username: containerRegistryName
          passwordSecretRef: 'container-registry-password'
        }
      ] : null
      ingress: enableIngress ? {
        external: isExternalIngress
        targetPort: containerPort
        transport: 'auto'
      } : null
    }
    template: {
      containers: [
        {
          image: containerImage
          name: containerAppName
          env: env
          resources: {
            cpu: cpu
            memory: memory
          }

        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: 1
      }
    }
  }
}

output fqdn string = enableIngress ? containerApp.properties.configuration.ingress.fqdn : 'Ingress not enabled'
