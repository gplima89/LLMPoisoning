# Quick Start Guide - LLM Poisoning Workshop

This guide helps you get started quickly with the workshop materials.

## Prerequisites (5 minutes)

1. **Azure Subscription** with permissions to create:
   - Azure OpenAI Service
   - Azure AI Search
   - Azure Storage
   - Azure Key Vault

2. **Local Tools**:
   ```bash
   # Verify installations
   python --version  # 3.9+
   az --version      # Azure CLI
   git --version
   ```

## Quick Setup (15 minutes)

### Option A: Automated Setup (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/gplima89/LLMPoisoning.git
cd LLMPoisoning

# 2. Run Azure deployment
cd setup
chmod +x deploy-azure-resources.sh
./deploy-azure-resources.sh

# 3. Install Python dependencies
cd ..
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Initialize search index
python src/sample-app/init_search_index.py
python src/sample-app/load_sample_documents.py

# 5. Start application
python src/sample-app/app.py
```

Visit: http://localhost:5000

### Option B: Manual Setup

Follow detailed instructions in [docs/04-azure-setup.md](docs/04-azure-setup.md)

## Workshop Modules

### For Participants

1. **📚 Learn the Theory** (1 hour)
   - Read: [docs/01-theory.md](docs/01-theory.md)
   - Read: [docs/02-attack-types.md](docs/02-attack-types.md)
   - Read: [docs/03-microsoft-stack.md](docs/03-microsoft-stack.md)

2. **🔨 Hands-On Labs** (3 hours)
   - Lab 1: [Deploy Vulnerable App](labs/lab1-vulnerable-app.md)
   - Lab 2: Execute RAG Poisoning (scenarios/01-data-poisoning)
   - Lab 3: Test Prompt Injection (scenarios/02-prompt-injection)

3. **🛡️ Implement Protections** (2 hours)
   - Read: [protection/01-input-validation.md](protection/01-input-validation.md)
   - Implement protections in your app
   - Test effectiveness

### For Instructors

- Review: [docs/WORKSHOP_GUIDE.md](docs/WORKSHOP_GUIDE.md)
- 8-hour workshop agenda with timing
- Facilitation tips and troubleshooting
- Assessment and feedback mechanisms

## Key Commands

```bash
# Test baseline (before attack)
cd scenarios/01-data-poisoning
python test_before_poisoning.py

# Execute poisoning attack
python poison_rag.py

# Test compromised system (after attack)
python test_after_poisoning.py

# Cleanup poisoned data
python cleanup.py

# Start web application
cd ../../src/sample-app
python app.py
```

## Testing the Setup

Quick verification:

```bash
# Test Azure OpenAI
python << EOF
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
response = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    messages=[{"role": "user", "content": "Say 'Setup OK'"}]
)
print(response.choices[0].message.content)
EOF
```

Expected output: "Setup OK" or similar

## Common Issues

### "Module not found" errors
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Azure authentication fails
```bash
az login
az account set --subscription "your-subscription-id"
```

### Port 5000 already in use
```bash
export PORT=5001
python app.py
```

### Search index errors
```bash
python src/sample-app/init_search_index.py
```

## Project Structure

```
LLMPoisoning/
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
├── .env.example                 # Configuration template
│
├── docs/                        # Theory and guides
│   ├── 01-theory.md            # LLM poisoning concepts
│   ├── 02-attack-types.md      # Attack classifications
│   ├── 03-microsoft-stack.md   # Azure AI architecture
│   ├── 04-azure-setup.md       # Resource deployment
│   ├── 05-dev-setup.md         # Local environment
│   └── WORKSHOP_GUIDE.md       # Instructor guide
│
├── scenarios/                   # Attack demonstrations
│   ├── 01-data-poisoning/      # RAG poisoning
│   │   ├── README.md
│   │   ├── poison_rag.py
│   │   ├── test_before_poisoning.py
│   │   ├── test_after_poisoning.py
│   │   └── cleanup.py
│   └── 02-prompt-injection/    # Prompt attacks
│       └── README.md
│
├── protection/                  # Security strategies
│   └── 01-input-validation.md  # Input protection
│
├── labs/                        # Hands-on exercises
│   └── lab1-vulnerable-app.md
│
├── src/sample-app/             # Demo application
│   ├── app.py                  # Flask web app
│   ├── chatbot.py              # RAG chatbot
│   ├── init_search_index.py    # Index setup
│   └── load_sample_documents.py # Data loading
│
└── setup/                       # Deployment
    └── deploy-azure-resources.sh
```

## Learning Path

### Beginner Path (4 hours)
1. Read theory documentation
2. Deploy sample application
3. Execute RAG poisoning attack
4. Review protection strategies

### Intermediate Path (6 hours)
1. Complete beginner path
2. Test prompt injection scenarios
3. Implement input validation
4. Configure monitoring

### Advanced Path (8+ hours)
1. Complete intermediate path
2. Create custom attack scenarios
3. Implement complete protection suite
4. Design secure RAG architecture

## Resources

### Microsoft Documentation
- [Azure OpenAI](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-studio/)

### Security Resources
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Microsoft AI Security](https://www.microsoft.com/security/business/ai-machine-learning)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

## Getting Help

### During Workshop
- Ask your instructor
- Check troubleshooting sections in docs
- Collaborate with peers

### After Workshop
- Open GitHub issues for bugs
- Check existing documentation
- Review Azure documentation

## Cleanup

After completing the workshop:

```bash
# Delete all Azure resources
az group delete --name llm-poisoning-workshop-rg --yes

# This will delete:
# - Azure OpenAI Service
# - Azure AI Search
# - Storage Account
# - Key Vault
# - Log Analytics
# - Application Insights
```

**Estimated cost if left running**: ~$300-400/month

## Next Steps

1. ✅ Complete quick setup
2. ✅ Test basic functionality
3. ✅ Start with theory modules
4. ✅ Work through hands-on labs
5. ✅ Implement protections
6. ✅ Clean up resources

## Support

For issues or questions:
- GitHub Issues: https://github.com/gplima89/LLMPoisoning/issues
- Workshop discussions: Use GitHub Discussions

---

**Ready to start?** Begin with [docs/01-theory.md](docs/01-theory.md)

**Want hands-on immediately?** Jump to [labs/lab1-vulnerable-app.md](labs/lab1-vulnerable-app.md)

**Instructor preparing workshop?** Review [docs/WORKSHOP_GUIDE.md](docs/WORKSHOP_GUIDE.md)
