# AI Foundry Models to Excel

This tool exports all available models from Azure AI Foundry (Model Catalog) and Azure ML Registries to an Excel file with detailed information about each model.

## Features

- Fetches all available models from Azure AI Foundry (Model Catalog) using the official Account Management API
- Fetches all available models from Azure ML Registries (azureml, azureml-meta, azureml-cohere, azureml-mistral, azureml-xai, azureml-deepseek, azureml-core42, azureml-stabilityai, azureml-nvidia, HuggingFace, azureml-gretel, etc.) for managed compute deployment
- Exports model details including name, version, description, format, kind, SKU, lifecycle status, and system metadata
- Generates a formatted Excel file with:
  - Color-coded headers
  - Auto-adjusted column widths
  - Frozen header row for easy scrolling
  - Timestamp in filename
  - Source identification for each model (AI Foundry Catalog vs Azure ML Registry)

## Prerequisites

- Python 3.8 or higher
- Azure subscription with access to AI Foundry
- Appropriate Azure permissions to list models in the region

## Installation

1. Clone this repository:
```bash
git clone https://github.com/tannenbaum-gmbh/ai-foundry-models-to-excel.git
cd ai-foundry-models-to-excel
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Azure credentials:
```bash
cp .env.example .env
```

4. Edit `.env` and fill in your Azure details:
```
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_LOCATION=eastus

# Optional: Azure ML Registry Names (comma-separated list)
# See REGISTRY_DISCOVERY.md for the complete list of available registries
# Common registries: azureml, azureml-meta, azureml-cohere, azureml-mistral, azureml-xai, azureml-deepseek, azureml-core42, azureml-stabilityai, azureml-nvidia, HuggingFace, azureml-gretel
AZURE_ML_REGISTRY_NAMES=azureml,azureml-meta,azureml-cohere,azureml-mistral,azureml-xai,azureml-deepseek,azureml-core42,azureml-stabilityai,azureml-nvidia,HuggingFace,azureml-gretel
```

Note: Replace `eastus` with your desired Azure region (e.g., `westus`, `westeurope`, etc.)

The `AZURE_ML_REGISTRY_NAMES` environment variable is optional and defaults to `azureml,azureml-meta,azureml-cohere,azureml-mistral,azureml-xai,HuggingFace,azureml-nvidia` if not specified. You can customize this list to include other Azure ML registries as needed.

For a complete list of available registries and how they were discovered, see [REGISTRY_DISCOVERY.md](REGISTRY_DISCOVERY.md). You can also run `python3 discover_registries.py` to test which registries are accessible with your Azure credentials.

## Authentication

This tool uses Azure's `DefaultAzureCredential`, which supports multiple authentication methods in order:

1. Environment variables
2. Managed Identity
3. Visual Studio Code
4. Azure CLI
5. Azure PowerShell
6. Interactive browser

The easiest way for local development is to use Azure CLI:

```bash
az login
```

## Usage

Run the script to export models:

```bash
python export_models.py
```

The script will:
1. Connect to Azure using the AI Foundry Account Management API
2. Fetch all available models from the AI Foundry catalog in the specified region
3. Fetch all available models from the configured Azure ML Registries
4. Generate an Excel file named `ai_foundry_models_YYYYMMDD_HHMMSS.xlsx`

## Output

The Excel file contains the following columns:

- **Source**: Model source (AI Foundry Catalog or Azure ML Registry name)
- **Name**: Model name
- **Version**: Model version
- **Description**: Model description
- **Format**: Model format (e.g., OpenAI, MLflow, Custom)
- **Kind**: Model kind/type
- **SKU**: Model SKU name
- **Lifecycle Status**: Model lifecycle status (e.g., Stable, Preview)
- **Max Capacity**: Maximum capacity for the model
- **Created Date**: When the model was created
- **Created By**: Who created the model
- **Last Modified Date**: When the model was last modified
- **Last Modified By**: Who last modified the model

### Model Sources

The tool fetches models from two sources:

1. **AI Foundry Catalog**: Models available through the AI Foundry Model Catalog for standard deployments with pay-as-you-go billing
2. **Azure ML Registries**: Models available through [Azure Machine Learning registries](https://learn.microsoft.com/en-us/azure/machine-learning/foundry-models-overview?view=azureml-api-2#managed-compute) for managed compute deployment, including:
   - `azureml`: Main Azure ML registry (Microsoft/Phi models)
   - `azureml-meta`: Meta/Llama models
   - `azureml-cohere`: Cohere models
   - `azureml-mistral`: Mistral models
   - `azureml-xai`: xAI models (Grok)
   - `azureml-deepseek`: DeepSeek models (DeepSeek-R1, DeepSeek-V3)
   - `azureml-core42`: Core42 models (Jais - Arabic/English)
   - `azureml-stabilityai`: Stability AI models (Stable Diffusion, Stable Image)
   - `azureml-nvidia`: NVIDIA models
   - `HuggingFace`: Hugging Face models
   - `azureml-gretel`: Gretel models
   - And other specialized registries
   
   For a complete list and descriptions, see [REGISTRY_DISCOVERY.md](REGISTRY_DISCOVERY.md).

## GitHub Actions Workflow

This repository includes a GitHub Actions workflow that automatically exports AI Foundry models and creates a release with the Excel file.

### Setup

To use the automated workflow, configure the following GitHub secrets in your repository settings:

#### Azure OIDC Authentication
- `AZURE_CLIENT_ID`: The client ID of your Azure AD application
- `AZURE_TENANT_ID`: Your Azure AD tenant ID
- `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID

#### Azure AI Foundry Configuration
- `AZURE_LOCATION`: Your Azure region (e.g., `eastus`, `westus`, `westeurope`)
- `AZURE_ML_REGISTRY_NAMES`: (Optional) Comma-separated list of Azure ML Registry names (defaults to `azureml,azureml-meta,azureml-cohere,azureml-mistral,azureml-xai,HuggingFace,azureml-nvidia`). See [REGISTRY_DISCOVERY.md](REGISTRY_DISCOVERY.md) for all available registries.

### Azure OIDC Setup

1. Create an Azure AD application registration
2. Configure federated credentials for GitHub Actions
3. Grant the application appropriate permissions (Reader role at subscription level or appropriate scope)
4. Add the credentials as GitHub secrets

For detailed instructions, see [Azure's documentation on configuring OIDC for GitHub Actions](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure).

### API Reference

This tool uses:
- [AI Foundry Account Management REST API - Models List](https://learn.microsoft.com/en-us/rest/api/aifoundry/accountmanagement/models/list?view=rest-aifoundry-accountmanagement-2025-06-01&tabs=HTTP) to retrieve models from the AI Foundry catalog
- [Azure ML Python SDK](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python) to retrieve models from Azure ML registries

For more information about deployment options, see [Azure AI Foundry Models Overview](https://learn.microsoft.com/en-us/azure/machine-learning/foundry-models-overview?view=azureml-api-2#deployment-options).

### Workflow Triggers

The workflow can be triggered in two ways:

1. **Manual trigger**: Go to Actions → Export AI Foundry Models → Run workflow
2. **Scheduled**: Automatically runs every Monday at 6:00 AM UTC

### Workflow Steps

The workflow performs the following steps:

1. Checks out the repository code
2. Sets up Python 3.11 environment
3. Installs dependencies from requirements.txt
4. Authenticates to Azure using OIDC
5. Runs the export_models.py script
6. Uploads the generated Excel file as a workflow artifact (retained for 90 days)
7. Creates a GitHub release with the Excel file attached

### Accessing the Results

After the workflow completes:
- Download the Excel file from the workflow run's artifacts section
- Find the release in the Releases section with the Excel file attached

## Troubleshooting

### Authentication Errors

If you encounter authentication errors:
- Ensure you're logged in with `az login`
- Verify your Azure credentials have appropriate permissions to list models
- Check that the subscription ID and location are correct

### No Models Found

If no models are found:
- Verify that the specified Azure location/region has AI Foundry models available
- Check that you have read permissions on the subscription or appropriate scope
- Ensure you're using a valid Azure region (e.g., `eastus`, `westus`, `westeurope`)

### GitHub Actions Workflow Errors

If the GitHub Actions workflow fails:
- Verify all required secrets are configured correctly (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_LOCATION`)
- Check that the Azure OIDC federated credentials are set up properly
- Ensure the Azure application has the necessary permissions (Reader role) on the subscription or appropriate scope
- Review the workflow logs for specific error messages

## License

MIT License - see [LICENSE](LICENSE) file for details