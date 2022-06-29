#!/bin/bash

CONTAINER_NAME=$1
az acr login --name $CONTAINER_NAME

docker build -t accounts ./src/accounts 
docker tag accounts $CONTAINER_NAME.azurecr.io/accounts:latest
docker push $CONTAINER_NAME.azurecr.io/accounts:latest

docker build -t payments ./src/payments 
docker tag accounts $CONTAINER_NAME.azurecr.io/payments:latest
docker push $CONTAINER_NAME.azurecr.io/payments:latest