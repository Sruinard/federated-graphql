#!/bin/bash

RESOURCE_GROUP=$1
ENDPOINT=$(az deployment group show -g ${RESOURCE_GROUP} -n main --query properties.outputs.graphqlEndpoint.value)
echo $ENDPOINT | xargs get-graphql-schema > schema.graphql