# Azure ML Registry Discovery

This document explains the Azure ML registries available for the AI Foundry Models to Excel tool and how they were discovered.

## Background

The Azure AI Foundry model catalog (https://ai.azure.com/explore/models) displays models organized by "Collections" which represent different model providers. These collections correspond to Azure Machine Learning registries that host the models.

## Collections in Azure AI Foundry UI

Based on the Azure AI Foundry model catalog webpage, the following collections are visible in the UI:

- **Core42** - Bilingual Arabic/English LLMs (Jais models)
- **DeepSeek** - DeepSeek reasoning and language models
- **Meta** - Meta/Llama models
- **Microsoft** - Microsoft models including Phi, MAI, and others
- **Mistral AI** - Mistral models
- **OpenAI** - OpenAI models (GPT series)
- **Stability AI** - Image generation models (Stable Diffusion, Stable Image)
- **xAI** - Grok models

## Registry Names Mapping

The collections in the UI map to Azure ML registry names as follows:

| Collection (UI) | Registry Name | Models | Documentation |
|----------------|---------------|--------|---------------|
| Microsoft | `azureml` | Phi, MAI, and other Microsoft models | [Link](https://learn.microsoft.com/en-us/azure/machine-learning/concept-models-featured?view=azureml-api-2#microsoft) |
| Meta | `azureml-meta` | Llama models | [Link](https://learn.microsoft.com/en-us/azure/machine-learning/concept-models-featured?view=azureml-api-2#meta) |
| Cohere | `azureml-cohere` | Cohere command and rerank models | [Link](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-from-partners#cohere) |
| Mistral AI | `azureml-mistral` | Mistral models | - |
| xAI | `azureml-xai` | Grok models | - |
| DeepSeek | `azureml-deepseek` | DeepSeek-R1, DeepSeek-V3 | [Link](https://learn.microsoft.com/en-us/azure/machine-learning/concept-models-featured?view=azureml-api-2#deepseek) |
| Core42 | `azureml-core42` | Jais (Arabic/English) | [Link](https://learn.microsoft.com/en-us/azure/machine-learning/concept-models-featured?view=azureml-api-2#core42) |
| Stability AI | `azureml-stabilityai` | Stable Diffusion, Stable Image | [Link](https://learn.microsoft.com/en-us/azure/machine-learning/concept-models-featured?view=azureml-api-2#stability-ai) |
| NVIDIA | `azureml-nvidia` | NVIDIA models | - |
| Hugging Face | `HuggingFace` | Various Hugging Face models | - |
| Gretel | `azureml-gretel` | Gretel Navigator models | [Link](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/model-lifecycle-retirement#timelines-for-foundry-models) |

**Note about OpenAI models:** OpenAI models (GPT series) are primarily available through the Azure OpenAI service integration rather than as a separate Azure ML registry. They may be available in the main `azureml` registry or require a different deployment approach.

## Discovery Method

The registry names were discovered through the following methods:

1. **Official Microsoft Documentation**: The primary source was the official Microsoft Learn documentation, specifically:
   - [Featured models of Azure AI model catalog](https://learn.microsoft.com/en-us/azure/machine-learning/concept-models-featured)
   - [Foundry Models from partners and community](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-from-partners)

2. **Model Card URLs**: Individual model cards in the documentation contain the registry name in the URL format:
   ```
   https://ai.azure.com/explore/models/{model-name}/version/{version}/registry/{registry-name}
   ```

3. **Programmatic Testing**: The `discover_registries.py` script attempts to connect to each registry and list models to verify accessibility.

## Using the Discovery Script

To discover available registries and test their accessibility, run:

```bash
python3 discover_registries.py
```

**Prerequisites:**
- Python 3.8+
- Installed dependencies: `pip install -r requirements.txt`
- Azure authentication configured (Azure CLI login or other DefaultAzureCredential methods)

The script will:
1. Test each known registry name
2. Attempt to list models from each registry
3. Report which registries are accessible
4. Provide sample model names from accessible registries
5. Generate a recommended registry list for the `.env` file

## Confirmed Registry List

Based on official Microsoft documentation, the following registries are confirmed to exist:

```
AZURE_ML_REGISTRY_NAMES=azureml,azureml-meta,azureml-cohere,azureml-mistral,azureml-xai,azureml-deepseek,azureml-core42,azureml-stabilityai,azureml-nvidia,HuggingFace,azureml-gretel
```

**Previous default list (may include some registries that don't exist):**
```
AZURE_ML_REGISTRY_NAMES=azureml,azureml-meta,azureml-cohere,azureml-mistral,azureml-xai,HuggingFace,azureml-nvidia
```

## References

1. [Azure AI Foundry Models Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/foundry-models-overview)
2. [Featured models of Azure AI model catalog](https://learn.microsoft.com/en-us/azure/machine-learning/concept-models-featured)
3. [Foundry Models from partners and community](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-from-partners)
4. [Azure Machine Learning registries](https://learn.microsoft.com/en-us/azure/machine-learning/concept-machine-learning-registries-mlops)
5. [Model catalog in Azure AI Foundry portal](https://ai.azure.com/explore/models)

## Notes

- Registry accessibility may depend on your Azure subscription, permissions, and regional availability.
- Some registries may require specific access permissions or marketplace subscriptions.
- The list of available registries may change over time as Microsoft adds or retires model providers.
- Not all collections visible in the UI may have corresponding public registries accessible via the Python SDK.
