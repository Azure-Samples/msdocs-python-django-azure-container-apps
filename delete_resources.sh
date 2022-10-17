#!/bin/bash

# This script deletes the resources created in the tutorial https://learn.microsoft.com/azure/developer/python/tutorial-deploy-python-web-app-azure-container-apps-01
# Make sure you are logged in to Azure. If unsure, run "az login" before using this script.

echo "Where is the name of the resource group to delete?"
read RESOURCE_GROUP

az group delete --name $RESOURCE_GROUP --yes
echo "INFO:: Deleted resource group: $RESOURCE_GROUP."

