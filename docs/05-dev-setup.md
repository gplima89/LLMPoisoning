# Module 5: Development Environment Configuration

## Local Development Setup

This guide covers setting up your local development environment for the LLM Poisoning Workshop.

## Prerequisites

### Required Software

1. **Python 3.9+**
```bash
python --version  # Should be 3.9 or higher
```

2. **pip and virtualenv**
```bash
pip install --upgrade pip
pip install virtualenv
```

3. **Git**
```bash
git --version
```

4. **Azure CLI**
```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'

# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify
az --version
```

5. **Visual Studio Code (Optional but Recommended)**
```bash
# Download from https://code.visualstudio.com/
# Install recommended extensions:
# - Python
# - Azure Tools
# - Pylance
# - Azure AI Tools
```

## Python Environment Setup

### Create Virtual Environment

```bash
cd /path/to/LLMPoisoning

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Verify
which python  # Should point to venv/bin/python
```

### Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list | grep -E "openai|azure|langchain"
```

## Configuration Files

### 1. Environment Variables

Create `.env` file in the project root:

```bash
# Copy example file
cp .env.example .env

# Edit with your Azure credentials
# Use your favorite editor
nano .env  # or vim, vscode, etc.
```

Required environment variables:

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt4-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_API_KEY=your-search-key-here
AZURE_SEARCH_INDEX_NAME=documents-index

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...

# Azure Key Vault
AZURE_KEYVAULT_URL=https://your-keyvault.vault.azure.net/

# Application Insights
APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=...

# Workshop Configuration
WORKSHOP_MODE=demo
ENABLE_VULNERABILITIES=true
ENABLE_PROTECTIONS=false
LOG_LEVEL=INFO
```

### 2. Azure Configuration

Authenticate with Azure:

```bash
# Login to Azure
az login

# Set default subscription
az account set --subscription "your-subscription-id"

# Verify
az account show
```

### 3. Git Configuration

Configure Git to ignore sensitive files:

```bash
# .gitignore is already configured, verify:
cat .gitignore
```

Ensure `.env` is in `.gitignore`:

```bash
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".vscode/" >> .gitignore
```

## IDE Configuration

### Visual Studio Code

#### Recommended Extensions

Install these extensions:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-toolsai.jupyter",
    "ms-azuretools.vscode-azureappservice",
    "ms-azuretools.vscode-azurefunctions",
    "ms-azuretools.vscode-cosmosdb",
    "GitHub.copilot",
    "GitHub.copilot-chat"
  ]
}
```

#### Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask App",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "src/sample-app/app.py",
        "FLASK_ENV": "development"
      },
      "args": ["run", "--no-debugger", "--no-reload"],
      "jinja": true
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env"
    }
  ]
}
```

#### Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

## Jupyter Notebook Setup

For interactive demonstrations:

```bash
# Install Jupyter
pip install jupyter notebook ipykernel

# Create kernel
python -m ipykernel install --user --name=llm-poisoning

# Start Jupyter
jupyter notebook
```

## Testing the Setup

### 1. Test Azure OpenAI Connection

Create `test_setup.py`:

```python
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

def test_openai():
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": "Hello!"}]
    )
    
    print("✅ Azure OpenAI connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    return True

if __name__ == "__main__":
    try:
        test_openai()
    except Exception as e:
        print(f"❌ Error: {e}")
```

Run the test:

```bash
python test_setup.py
```

### 2. Test Azure AI Search Connection

```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

def test_search():
    search_client = SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
    )
    
    results = list(search_client.search("test", top=1))
    print("✅ Azure AI Search connection successful!")
    print(f"Index accessible. Documents: {len(results)}")
    return True

if __name__ == "__main__":
    try:
        test_search()
    except Exception as e:
        print(f"❌ Error: {e}")
```

### 3. Run All Tests

```bash
# Run test suite
python -m pytest tests/ -v

# Expected output:
# tests/test_setup.py::test_azure_openai PASSED
# tests/test_setup.py::test_azure_search PASSED
# tests/test_setup.py::test_storage PASSED
```

## Directory Structure

Your development environment should look like this:

```
LLMPoisoning/
├── .env                      # Local environment variables (not in git)
├── .env.example              # Template for .env
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── venv/                     # Virtual environment (not in git)
├── docs/                     # Documentation
├── src/
│   ├── sample-app/          # Demo application
│   ├── scenarios/           # Attack scenarios
│   └── utils/               # Utility modules
├── tests/                   # Test suite
├── labs/                    # Hands-on lab materials
├── scenarios/               # Detailed scenarios
└── protection/              # Protection strategies
```

## Development Workflow

### Daily Workflow

1. **Activate environment**:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. **Pull latest changes**:
```bash
git pull origin main
```

3. **Install new dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run application**:
```bash
cd src/sample-app
python app.py
```

5. **Make changes and test**:
```bash
# Edit files
# Run tests
pytest tests/

# Run linting
pylint src/
black src/
```

6. **Commit changes**:
```bash
git add .
git commit -m "Description of changes"
git push
```

## Troubleshooting

### Common Issues

#### Issue: Import errors for Azure packages
```bash
# Solution: Reinstall packages
pip uninstall azure-ai-openai azure-search-documents
pip install --no-cache-dir azure-ai-openai azure-search-documents
```

#### Issue: SSL certificate errors
```bash
# Windows: Update certifi
pip install --upgrade certifi

# macOS: Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

#### Issue: Environment variables not loading
```bash
# Check .env file exists
ls -la .env

# Verify python-dotenv is installed
pip list | grep python-dotenv

# Load manually in Python
from dotenv import load_dotenv
load_dotenv(override=True)
```

#### Issue: Azure authentication fails
```bash
# Re-authenticate
az logout
az login
az account show
```

## Best Practices

1. **Always use virtual environment** - Never install packages globally
2. **Keep .env out of git** - Never commit credentials
3. **Update dependencies regularly** - `pip install --upgrade -r requirements.txt`
4. **Run tests before committing** - Ensure nothing is broken
5. **Use meaningful commit messages** - Help others understand changes
6. **Document as you go** - Update docs with changes

## Next Steps

With your development environment configured, proceed to [Module 6: Sample Application Deployment](06-app-deployment.md) to deploy the demo application.

## Quick Reference

### Essential Commands

```bash
# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/sample-app/app.py

# Run tests
pytest tests/

# Run linting
pylint src/
black src/

# Azure login
az login
```

### Useful Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Azure SDK for Python](https://learn.microsoft.com/python/azure/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
