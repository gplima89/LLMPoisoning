# Module 4: Azure Resource Setup

## Prerequisites Checklist

Before beginning, ensure you have:

- [ ] Azure subscription with Owner or Contributor role
- [ ] Azure CLI installed (`az --version`)
- [ ] Python 3.9 or later
- [ ] Git installed
- [ ] Visual Studio Code (recommended)
- [ ] Sufficient Azure quota for:
  - Azure OpenAI (GPT-4 deployment)
  - Azure AI Search (Standard tier)
  - Azure Container Apps
  - Azure Storage

## Resource Overview

This workshop requires the following Azure resources:

| Resource | Purpose | Estimated Cost |
|----------|---------|----------------|
| Azure OpenAI | LLM hosting | ~$10-50/day |
| Azure AI Search | RAG knowledge base | ~$250/month |
| Azure Storage | Data and logs | ~$1/month |
| Azure Container Apps | Application hosting | ~$10/month |
| Azure Monitor | Logging and alerts | ~$5/month |
| Azure Key Vault | Secrets management | ~$1/month |

**Total Estimated Cost**: ~$300-400/month during active workshop use

## Automated Setup

### Option 1: Quick Setup Script

```bash
# Clone the repository
git clone https://github.com/gplima89/LLMPoisoning.git
cd LLMPoisoning/setup

# Make script executable
chmod +x deploy-azure-resources.sh

# Run deployment (takes ~10-15 minutes)
./deploy-azure-resources.sh
```

The script will:
1. Prompt for Azure subscription and region
2. Create resource group
3. Deploy all required resources
4. Configure security settings
5. Output configuration file

### Option 2: Azure Portal (Manual)

For those who prefer manual setup or want more control:

#### Step 1: Create Resource Group

```bash
az login
az account set --subscription "your-subscription-id"

az group create \
  --name llm-poisoning-workshop-rg \
  --location eastus
```

#### Step 2: Deploy Azure OpenAI

```bash
az cognitiveservices account create \
  --name llm-poisoning-openai \
  --resource-group llm-poisoning-workshop-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --yes

# Deploy GPT-4 model
az cognitiveservices account deployment create \
  --name llm-poisoning-openai \
  --resource-group llm-poisoning-workshop-rg \
  --deployment-name gpt4-deployment \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-name "Standard" \
  --capacity 10
```

#### Step 3: Deploy Azure AI Search

```bash
az search service create \
  --name llm-poisoning-search \
  --resource-group llm-poisoning-workshop-rg \
  --sku standard \
  --location eastus \
  --partition-count 1 \
  --replica-count 1
```

#### Step 4: Create Storage Account

```bash
az storage account create \
  --name llmpoisoningstorage \
  --resource-group llm-poisoning-workshop-rg \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# Create containers
az storage container create \
  --name training-data \
  --account-name llmpoisoningstorage

az storage container create \
  --name poisoned-data \
  --account-name llmpoisoningstorage
```

#### Step 5: Create Key Vault

```bash
az keyvault create \
  --name llm-poisoning-kv \
  --resource-group llm-poisoning-workshop-rg \
  --location eastus

# Store secrets
OPENAI_KEY=$(az cognitiveservices account keys list \
  --name llm-poisoning-openai \
  --resource-group llm-poisoning-workshop-rg \
  --query key1 -o tsv)

az keyvault secret set \
  --vault-name llm-poisoning-kv \
  --name openai-api-key \
  --value $OPENAI_KEY

SEARCH_KEY=$(az search admin-key show \
  --service-name llm-poisoning-search \
  --resource-group llm-poisoning-workshop-rg \
  --query primaryKey -o tsv)

az keyvault secret set \
  --vault-name llm-poisoning-kv \
  --name search-api-key \
  --value $SEARCH_KEY
```

#### Step 6: Setup Monitoring

```bash
az monitor log-analytics workspace create \
  --resource-group llm-poisoning-workshop-rg \
  --workspace-name llm-poisoning-logs \
  --location eastus

az monitor app-insights component create \
  --app llm-poisoning-insights \
  --location eastus \
  --resource-group llm-poisoning-workshop-rg \
  --workspace llm-poisoning-logs
```

## Security Configuration

### 1. Enable Private Endpoints

```bash
# Create VNet
az network vnet create \
  --name llm-poisoning-vnet \
  --resource-group llm-poisoning-workshop-rg \
  --address-prefix 10.0.0.0/16 \
  --subnet-name default \
  --subnet-prefix 10.0.0.0/24

# Private endpoint for OpenAI
az network private-endpoint create \
  --name openai-private-endpoint \
  --resource-group llm-poisoning-workshop-rg \
  --vnet-name llm-poisoning-vnet \
  --subnet default \
  --private-connection-resource-id $(az cognitiveservices account show \
    --name llm-poisoning-openai \
    --resource-group llm-poisoning-workshop-rg \
    --query id -o tsv) \
  --group-id account \
  --connection-name openai-connection
```

### 2. Configure RBAC

```bash
# Get your user ID
USER_ID=$(az ad signed-in-user show --query id -o tsv)

# Grant access to OpenAI
az role assignment create \
  --role "Cognitive Services OpenAI User" \
  --assignee $USER_ID \
  --scope $(az cognitiveservices account show \
    --name llm-poisoning-openai \
    --resource-group llm-poisoning-workshop-rg \
    --query id -o tsv)

# Grant access to Search
az role assignment create \
  --role "Search Index Data Contributor" \
  --assignee $USER_ID \
  --scope $(az search service show \
    --name llm-poisoning-search \
    --resource-group llm-poisoning-workshop-rg \
    --query id -o tsv)
```

### 3. Enable Diagnostic Logging

```bash
# Get workspace ID
WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group llm-poisoning-workshop-rg \
  --workspace-name llm-poisoning-logs \
  --query id -o tsv)

# Enable OpenAI diagnostics
az monitor diagnostic-settings create \
  --name openai-diagnostics \
  --resource $(az cognitiveservices account show \
    --name llm-poisoning-openai \
    --resource-group llm-poisoning-workshop-rg \
    --query id -o tsv) \
  --workspace $WORKSPACE_ID \
  --logs '[{"category":"Audit","enabled":true},{"category":"RequestResponse","enabled":true}]' \
  --metrics '[{"category":"AllMetrics","enabled":true}]'
```

### 4. Configure Content Filters

```bash
# Content filters are configured via Azure Portal
# Navigate to: Azure OpenAI Studio > Content Filters
# Create custom filter with:
# - Violence: Medium
# - Hate: Medium  
# - Sexual: Medium
# - Self-harm: Medium
# - Jailbreak: High (if available)
```

## Environment Configuration

### Create .env file

```bash
cat > ../.env << EOF
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://llm-poisoning-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=\${OPENAI_KEY}
AZURE_OPENAI_DEPLOYMENT=gpt4-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://llm-poisoning-search.search.windows.net
AZURE_SEARCH_API_KEY=\${SEARCH_KEY}
AZURE_SEARCH_INDEX_NAME=documents-index

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING=\${STORAGE_CONN_STRING}
AZURE_STORAGE_CONTAINER=training-data

# Azure Key Vault Configuration
AZURE_KEYVAULT_URL=https://llm-poisoning-kv.vault.azure.net/

# Application Insights
APPINSIGHTS_CONNECTION_STRING=\${APPINSIGHTS_CONN_STRING}

# Workshop Configuration
WORKSHOP_MODE=demo
ENABLE_VULNERABILITIES=true
ENABLE_PROTECTIONS=false
EOF
```

## Verification

### Test Azure OpenAI Connection

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="gpt4-deployment",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Test Azure AI Search Connection

```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
)

# Should return empty results (no documents yet)
results = list(search_client.search("test"))
print(f"Index connected. Document count: {len(results)}")
```

## Cleanup

When workshop is complete:

```bash
# Delete all resources
az group delete \
  --name llm-poisoning-workshop-rg \
  --yes \
  --no-wait

# Verify deletion
az group exists --name llm-poisoning-workshop-rg
```

## Troubleshooting

### Issue: OpenAI quota exceeded
**Solution**: Request quota increase via Azure Portal or use different region

### Issue: Search service creation fails
**Solution**: Check service name uniqueness and region availability

### Issue: Private endpoint DNS resolution
**Solution**: Configure Azure Private DNS Zone or use public endpoints for workshop

### Issue: RBAC permissions not working
**Solution**: Wait 5-10 minutes for propagation, or use API keys temporarily

## Cost Optimization Tips

1. **Use pay-per-use** instead of PTUs for OpenAI during workshop
2. **Scale down Search** to Basic tier if only demonstrating concepts
3. **Delete resources** immediately after workshop completion
4. **Use Azure Dev/Test** subscription if available
5. **Set budget alerts** in Azure Cost Management

## Next Steps

With Azure resources deployed, proceed to [Module 5: Development Environment Configuration](05-dev-setup.md) to set up your local development environment.

## References

- [Azure OpenAI Quickstart](https://learn.microsoft.com/azure/ai-services/openai/quickstart)
- [Azure AI Search Setup](https://learn.microsoft.com/azure/search/search-create-service-portal)
- [Azure Resource Manager Templates](https://learn.microsoft.com/azure/azure-resource-manager/templates/)
