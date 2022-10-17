#!/bin/bash

# This script creates the resources used in the tutorial https://learn.microsoft.com/azure/developer/python/tutorial-deploy-python-web-app-azure-container-apps-01
# Make sure you are logged in to Azure. If unsure, run "az login" before using this script.

# Define values.

echo "Where is the code located? (Use . for current directory.)"
read CODE_LOCATION

echo "Enter a password for the PostgreSQL database instance:"
read ADMIN_PASSWORD

echo "What location do you want for the resource group? Examples: eastus, southcentralus, westeurope, southeastasia, australiaeast, japaneast, brazilsouth"
read LOCATION

echo "Enter a target port the container communicates on, e.g., 8000 for Django or 5000 for Flask"
read TARGET_PORT

UNIQUE=$(echo $RANDOM | md5sum | head -c 6)
RESOURCE_GROUP="pythoncontainer-rg-"$UNIQUE
echo "INFO:: Here's the resource group that will be used: $RESOURCE_GROUP."
echo "INFO:: Delete this resource group to delete all resources used in this demo."

REGISTRY_NAME="registry"$UNIQUE
IMAGE_NAME="pythoncontainer:latest"
POSTGRESQL_NAME="postgresql-db-"$UNIQUE
ADMIN_USER="demoadmin"
CONTAINER_ENV_NAME="python-container-env"
CONTAINER_APP_NAME="python-container-app"

# Create resource group.

az group create \
--name $RESOURCE_GROUP \
--location $LOCATION
echo "INFO:: Created resource group: $RESOURE_GROUP."

# Create a container registry.

az acr create \
--resource-group $RESOURCE_GROUP \
--name $REGISTRY_NAME \
--sku Basic \
--admin-enabled
echo "INFO:: Created container registry: $REGISTRY_NAME."

az acr login --name $REGISTRY_NAME
echo "INFO:: Logged into container registry: $REGISTRY_NAME."

# Build image in Azure.

az acr build \
--registry $REGISTRY_NAME \
--resource-group $RESOURCE_GROUP \
--image $IMAGE_NAME $CODE_LOCATION
echo "INFO:: Completed building image: $IMAGE_NAME."

# Create PostgreSQL database server.

az postgres flexible-server create \
   --resource-group $RESOURCE_GROUP \
   --name $POSTGRESQL_NAME  \
   --location $LOCATION \
   --admin-user $ADMIN_USER \
   --admin-password $ADMIN_PASSWORD \
   --sku-name Standard_D2s_v3 \
   --public-access 0.0.0.0
echo "INFO:: Created PostgreSQL database server: $POSTGRESQL_NAME."

# Create a database on the PostgreSQL server.

az postgres flexible-server db create \
   --resource-group $RESOURCE_GROUP \
   --server-name $POSTGRESQL_NAME \
   --database-name restaurants_reviews
echo "INFO:: Completed creating database restaurants_reviews on PostgreSQL server: $POSTGRESQL_NAME."

# Deploy (make sure extension is added)

# Create a container apps environment.

az containerapp env create \
--name $CONTAINER_ENV_NAME \
--resource-group $RESOURCE_GROUP \
--location $LOCATION
echo "INFO:: Completed creating container apps environment: $CONTAINER_ENV_NAME."

# Get sign-in credentials for Azure Container Registry.

ACR_USERNAME=$(az acr credential show --name $REGISTRY_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $REGISTRY_NAME --query passwords[0].value --output tsv)

# Create container app.

ENV_VARS="AZURE_POSTGRESQL_HOST=$POSTGRESQL_NAME.postgres.database.azure.com AZURE_POSTGRESQL_DATABASE=restaurants_reviews AZURE_POSTGRESQL_USERNAME=$ADMIN_USER AZURE_POSTGRESQL_PASSWORD=$ADMIN_PASSWORD RUNNING_IN_PRODUCTION=1"
echo $ENV_VARS

az containerapp create \
--name $CONTAINER_APP_NAME \
--resource-group $RESOURCE_GROUP \
--image $REGISTRY_NAME.azurecr.io/$IMAGE_NAME \
--environment $CONTAINER_ENV_NAME \
--ingress external \
--target-port $TARGET_PORT \
--min-replicas 1 \
--registry-server $REGISTRY_NAME.azurecr.io \
--registry-username $ACR_USERNAME \
--registry-password $ACR_PASSWORD \
--env-vars $ENV_VARS \
--query properties.configuration.ingress.fqdn
echo "INFO:: Completed creating container app $CONTAINER_APP_NAME."

echo "INFO:: If using Django, connect to the container and migrate the schema."
echo "INFO:: Use the following command:"
echo "INFO:: az containerapp exec --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP"
echo "INFO:: Then, run 'python manage.py migrate'."
echo "INFO:: Then, type 'exit'."