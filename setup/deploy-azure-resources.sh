#!/bin/bash

# LLM Poisoning Workshop - Azure Resource Deployment Script
# This script deploys all required Azure resources for the workshop

set -e  # Exit on error

echo "================================================================"
echo "LLM Poisoning Workshop - Azure Resource Deployment"
echo "================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP_NAME="llm-poisoning-workshop-rg"
LOCATION="eastus"
OPENAI_NAME="llm-poisoning-openai-$RANDOM"
SEARCH_NAME="llm-poisoning-search-$RANDOM"
STORAGE_NAME="llmpoisonstorage$RANDOM"
KEYVAULT_NAME="llm-poison-kv-$RANDOM"
LOG_WORKSPACE_NAME="llm-poisoning-logs"
APPINSIGHTS_NAME="llm-poisoning-insights"

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed. Please install it first."
    echo "Visit: https://docs.microsoft.com/cli/azure/install-azure-cli"
    exit 1
fi

print_success "Azure CLI is installed"

# Login to Azure
print_info "Checking Azure login status..."
if ! az account show &> /dev/null; then
    print_info "Please login to Azure..."
    az login
fi

print_success "Logged in to Azure"

# Select subscription
print_info "Available subscriptions:"
az account list --output table

read -p "Enter subscription ID (or press Enter for default): " SUBSCRIPTION_ID

if [ ! -z "$SUBSCRIPTION_ID" ]; then
    az account set --subscription "$SUBSCRIPTION_ID"
    print_success "Subscription set to: $SUBSCRIPTION_ID"
fi

SUBSCRIPTION_ID=$(az account show --query id -o tsv)
print_info "Using subscription: $SUBSCRIPTION_ID"

# Confirm location
read -p "Enter Azure region (default: eastus): " USER_LOCATION
LOCATION=${USER_LOCATION:-$LOCATION}
print_info "Using location: $LOCATION"

# Create resource group
print_info "Creating resource group: $RESOURCE_GROUP_NAME"
az group create \
    --name "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --output none

print_success "Resource group created"

# Deploy Azure OpenAI
print_info "Deploying Azure OpenAI Service..."
az cognitiveservices account create \
    --name "$OPENAI_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --kind OpenAI \
    --sku S0 \
    --location "$LOCATION" \
    --yes \
    --output none

print_success "Azure OpenAI Service deployed"

# Deploy GPT-4 model
print_info "Deploying GPT-4 model..."
az cognitiveservices account deployment create \
    --name "$OPENAI_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --deployment-name gpt4-deployment \
    --model-name gpt-4 \
    --model-version "0613" \
    --model-format OpenAI \
    --sku-name "Standard" \
    --capacity 10 \
    --output none

print_success "GPT-4 model deployed"

# Deploy Azure AI Search
print_info "Deploying Azure AI Search..."
az search service create \
    --name "$SEARCH_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --sku standard \
    --location "$LOCATION" \
    --partition-count 1 \
    --replica-count 1 \
    --output none

print_success "Azure AI Search deployed"

# Create Storage Account
print_info "Creating Storage Account..."
az storage account create \
    --name "$STORAGE_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --sku Standard_LRS \
    --kind StorageV2 \
    --output none

print_success "Storage Account created"

# Create storage containers
print_info "Creating storage containers..."
STORAGE_KEY=$(az storage account keys list \
    --account-name "$STORAGE_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query '[0].value' -o tsv)

az storage container create \
    --name training-data \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --output none

az storage container create \
    --name poisoned-data \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --output none

print_success "Storage containers created"

# Create Key Vault
print_info "Creating Key Vault..."
az keyvault create \
    --name "$KEYVAULT_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --output none

print_success "Key Vault created"

# Store secrets in Key Vault
print_info "Storing secrets in Key Vault..."

OPENAI_KEY=$(az cognitiveservices account keys list \
    --name "$OPENAI_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query key1 -o tsv)

az keyvault secret set \
    --vault-name "$KEYVAULT_NAME" \
    --name openai-api-key \
    --value "$OPENAI_KEY" \
    --output none

SEARCH_KEY=$(az search admin-key show \
    --service-name "$SEARCH_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query primaryKey -o tsv)

az keyvault secret set \
    --vault-name "$KEYVAULT_NAME" \
    --name search-api-key \
    --value "$SEARCH_KEY" \
    --output none

print_success "Secrets stored in Key Vault"

# Create Log Analytics Workspace
print_info "Creating Log Analytics Workspace..."
az monitor log-analytics workspace create \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --workspace-name "$LOG_WORKSPACE_NAME" \
    --location "$LOCATION" \
    --output none

print_success "Log Analytics Workspace created"

# Create Application Insights
print_info "Creating Application Insights..."
az monitor app-insights component create \
    --app "$APPINSIGHTS_NAME" \
    --location "$LOCATION" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --workspace "$LOG_WORKSPACE_NAME" \
    --output none

print_success "Application Insights created"

# Get endpoints and keys
OPENAI_ENDPOINT="https://$OPENAI_NAME.openai.azure.com/"
SEARCH_ENDPOINT="https://$SEARCH_NAME.search.windows.net"
KEYVAULT_URL="https://$KEYVAULT_NAME.vault.azure.net/"

STORAGE_CONN_STRING=$(az storage account show-connection-string \
    --name "$STORAGE_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query connectionString -o tsv)

APPINSIGHTS_CONN_STRING=$(az monitor app-insights component show \
    --app "$APPINSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query connectionString -o tsv)

# Generate .env file
print_info "Generating .env file..."

cat > ../.env << EOF
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=$OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY=$OPENAI_KEY
AZURE_OPENAI_DEPLOYMENT=gpt4-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=$SEARCH_ENDPOINT
AZURE_SEARCH_API_KEY=$SEARCH_KEY
AZURE_SEARCH_INDEX_NAME=documents-index

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING=$STORAGE_CONN_STRING
AZURE_STORAGE_CONTAINER=training-data

# Azure Key Vault Configuration
AZURE_KEYVAULT_URL=$KEYVAULT_URL

# Application Insights
APPINSIGHTS_CONNECTION_STRING=$APPINSIGHTS_CONN_STRING

# Flask Configuration
FLASK_APP=src/sample-app/app.py
FLASK_ENV=development
FLASK_SECRET_KEY=$(openssl rand -hex 32)
PORT=5000

# Workshop Configuration
WORKSHOP_MODE=demo
ENABLE_VULNERABILITIES=true
ENABLE_PROTECTIONS=false
LOG_LEVEL=INFO
DEBUG=true
VERBOSE_LOGGING=true
EOF

print_success ".env file generated"

# Generate deployment summary
cat > deployment-summary.txt << EOF
================================================================
LLM Poisoning Workshop - Deployment Summary
================================================================

Deployment Date: $(date)
Subscription ID: $SUBSCRIPTION_ID
Location: $LOCATION

Resources Created:
------------------
Resource Group: $RESOURCE_GROUP_NAME
Azure OpenAI: $OPENAI_NAME
  - Endpoint: $OPENAI_ENDPOINT
  - Deployment: gpt4-deployment
  - Model: gpt-4 (0613)

Azure AI Search: $SEARCH_NAME
  - Endpoint: $SEARCH_ENDPOINT
  - SKU: Standard

Storage Account: $STORAGE_NAME
  - Containers: training-data, poisoned-data

Key Vault: $KEYVAULT_NAME
  - URL: $KEYVAULT_URL

Log Analytics: $LOG_WORKSPACE_NAME
Application Insights: $APPINSIGHTS_NAME

Estimated Monthly Cost: ~\$300-400

Next Steps:
-----------
1. Review the generated .env file
2. Install Python dependencies: pip install -r requirements.txt
3. Initialize search index: python src/sample-app/init_search_index.py
4. Start the application: python src/sample-app/app.py
5. Access the web interface: http://localhost:5000

Cleanup:
--------
To delete all resources:
az group delete --name $RESOURCE_GROUP_NAME --yes --no-wait

================================================================
EOF

print_success "Deployment summary saved to deployment-summary.txt"

echo ""
echo "================================================================"
echo -e "${GREEN}Deployment Complete!${NC}"
echo "================================================================"
echo ""
echo "Configuration saved to: ../.env"
echo "Summary saved to: deployment-summary.txt"
echo ""
print_info "Next steps:"
echo "  1. cd .."
echo "  2. source venv/bin/activate"
echo "  3. pip install -r requirements.txt"
echo "  4. python src/sample-app/init_search_index.py"
echo "  5. python src/sample-app/app.py"
echo ""
print_info "To clean up all resources:"
echo "  az group delete --name $RESOURCE_GROUP_NAME --yes"
echo ""
echo "================================================================"
