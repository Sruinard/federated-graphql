#!/bin/bash

CONTAINER_NAME=$1
az acr login --name $CONTAINER_NAME

docker build -t founders ./src/founders 
docker tag founders $CONTAINER_NAME.azurecr.io/founders:latest
docker push $CONTAINER_NAME.azurecr.io/founders:latest

docker build -t companies ./src/companies 
docker tag companies $CONTAINER_NAME.azurecr.io/companies:latest
docker push $CONTAINER_NAME.azurecr.io/companies:latest

docker build -t gateway ./src/gateway 
docker tag gateway $CONTAINER_NAME.azurecr.io/gateway:latest
docker push $CONTAINER_NAME.azurecr.io/gateway:latest