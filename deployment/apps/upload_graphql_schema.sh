#!/bin/bash

RESOURCE_GROUP=$1
ENDPOINT=$(az deployment group show -g ${RESOURCE_GROUP} -n main --query properties.outputs.graphqlEndpoint.value)
echo $ENDPOINT | xargs get-graphql-schema > schema.graphql
az apim api schema create --service-name $(az deployment group show -g ${RESOURCE_GROUP} -n main --query properties.outputs.apimName.value) \
    -g ${RESOURCE_GROUP} \
    -n main \
    --api-id $(az deployment group show -g ${RESOURCE_GROUP} -n main --query properties.outputs.apiId.value) \
    --schema-id graphql \
    --schema-type application/vnd.ms-azure-apim.graphql.schema \
    --schema-path ./schema.graphql