# AI Foundry Models to Excel

This tool exports all available models from Azure AI Foundry (Model Catalog) to an Excel file with detailed information about each model.

## Features

- Fetches all deployed models from Azure AI Foundry project
- Exports model deployment details including name, model name, version, publisher, type, SKU, capabilities, and connection information
- Generates a formatted Excel file with:
  - Color-coded headers
  - Auto-adjusted column widths
  - Frozen header row for easy scrolling
  - Timestamp in filename

## Prerequisites

- Python 3.8 or higher
- Azure subscription with AI Foundry project
- Appropriate Azure permissions to access the project

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

4. Edit `.env` and fill in your Azure AI Foundry project endpoint:
```
PROJECT_ENDPOINT=https://your-project-name.region.api.azureml.ms
```

You can find your project endpoint in the Azure AI Foundry portal:
- Navigate to your AI Foundry project
- Go to the "Overview" section
- Copy the "Project endpoint" value

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
1. Connect to your Azure AI Foundry project
2. Fetch all deployed models
3. Generate an Excel file named `ai_foundry_models_YYYYMMDD_HHMMSS.xlsx`

## Output

The Excel file contains the following columns:

- **Name**: Deployment name
- **Model Name**: The name of the deployed model
- **Model Version**: Model version
- **Model Publisher**: Publisher of the model (e.g., Microsoft, Meta, etc.)
- **Type**: Deployment type
- **SKU**: The pricing tier/SKU used for the deployment
- **Capabilities**: Model capabilities (e.g., chat, completion, embeddings)
- **Connection**: The connection name used for the deployment

## GitHub Actions Workflow

This repository includes a GitHub Actions workflow that automatically exports AI Foundry models and creates a release with the Excel file.

### Setup

To use the automated workflow, configure the following GitHub secrets in your repository settings:

#### Azure OIDC Authentication
- `AZURE_CLIENT_ID`: The client ID of your Azure AD application
- `AZURE_TENANT_ID`: Your Azure AD tenant ID
- `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID

#### Azure AI Foundry Configuration
- `PROJECT_ENDPOINT`: Your AI Foundry project endpoint (e.g., `https://your-project-name.region.api.azureml.ms`)

### Azure OIDC Setup

1. Create an Azure AD application registration
2. Configure federated credentials for GitHub Actions
3. Grant the application appropriate permissions to access your AI Foundry project
4. Add the credentials as GitHub secrets

For detailed instructions, see [Azure's documentation on configuring OIDC for GitHub Actions](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure).

**Note:** The application must have permissions to read deployments from the Azure AI Foundry project. The recommended role is "Azure AI Developer" or "Reader" on the AI Foundry project resource.

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
- Verify your Azure credentials have access to the AI Foundry project
- Check that the PROJECT_ENDPOINT is correct and matches your project endpoint in Azure

### No Models Found

If no models are found:
- Verify your AI Foundry project has deployed models (check "Models + endpoints" tab in the portal)
- Check that you have read permissions on the project
- Ensure you're connected to the correct project endpoint

### ParentResourceNotFound Error

If you encounter a `ParentResourceNotFound` error:
- This typically means you're using an Azure Machine Learning workspace instead of an Azure AI Foundry project
- Ensure you're using the correct PROJECT_ENDPOINT that points to an Azure AI Foundry project resource
- The endpoint should be in the format: `https://your-project-name.region.api.azureml.ms`

### GitHub Actions Workflow Errors

If the GitHub Actions workflow fails:
- Verify all required secrets are configured correctly
- Check that the Azure OIDC federated credentials are set up properly
- Ensure the Azure application has the necessary permissions to access the AI Foundry project (Azure AI Developer or Reader role)
- Verify that PROJECT_ENDPOINT is set correctly in GitHub secrets
- Review the workflow logs for specific error messages

## License

MIT License - see [LICENSE](LICENSE) file for details