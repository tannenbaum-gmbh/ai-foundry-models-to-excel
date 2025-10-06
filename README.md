# AI Foundry Models to Excel

This tool exports all available models from Azure AI Foundry (Model Catalog) to an Excel file with detailed information about each model.

## Features

- Fetches all models from Azure AI Foundry workspace
- Exports model details including name, version, description, tags, type, path, and creation information
- Generates a formatted Excel file with:
  - Color-coded headers
  - Auto-adjusted column widths
  - Frozen header row for easy scrolling
  - Timestamp in filename

## Prerequisites

- Python 3.8 or higher
- Azure subscription with AI Foundry workspace
- Appropriate Azure permissions to access the workspace

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
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_WORKSPACE_NAME=your-workspace-name
```

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
1. Connect to your Azure AI Foundry workspace
2. Fetch all available models
3. Generate an Excel file named `ai_foundry_models_YYYYMMDD_HHMMSS.xlsx`

## Output

The Excel file contains the following columns:

- **Name**: Model name
- **Version**: Model version
- **Description**: Model description
- **Tags**: Model tags (key:value pairs)
- **Type**: Model type
- **Path**: Model path/location
- **Created Date**: When the model was created
- **Created By**: Who created the model

## Troubleshooting

### Authentication Errors

If you encounter authentication errors:
- Ensure you're logged in with `az login`
- Verify your Azure credentials have access to the workspace
- Check that the subscription ID, resource group, and workspace name are correct

### No Models Found

If no models are found:
- Verify your workspace contains models
- Check that you have read permissions on the workspace
- Ensure you're connected to the correct workspace

## License

MIT License - see [LICENSE](LICENSE) file for details