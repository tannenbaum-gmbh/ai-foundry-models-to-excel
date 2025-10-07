#!/usr/bin/env python3
"""
Discover Available Azure ML Registries

This script attempts to discover available Azure ML public/system registries
by testing connections to known registry names and trying to list models.
"""

import sys
from typing import List, Dict, Any

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError


def test_registry(credential: DefaultAzureCredential, registry_name: str) -> Dict[str, Any]:
    """
    Test if a registry is accessible by attempting to connect and list models.
    
    Args:
        credential: Azure credential object
        registry_name: Name of the registry to test
        
    Returns:
        Dictionary with test results
    """
    result = {
        "name": registry_name,
        "accessible": False,
        "model_count": 0,
        "error": None,
        "sample_models": []
    }
    
    try:
        print(f"Testing registry: {registry_name}...")
        
        # Create MLClient for the registry
        ml_client = MLClient(credential=credential, registry_name=registry_name)
        
        # Try to list models (just get first few to verify access)
        models = ml_client.models.list()
        
        count = 0
        sample_models = []
        for model in models:
            count += 1
            if count <= 5:  # Get first 5 as samples
                sample_models.append(model.name if hasattr(model, 'name') else "N/A")
            if count >= 10:  # Stop after counting 10 to save time
                break
        
        result["accessible"] = True
        result["model_count"] = f"{count}+" if count >= 10 else count
        result["sample_models"] = sample_models
        
        print(f"  ✓ Accessible - Found {result['model_count']} models")
        if sample_models:
            print(f"    Sample models: {', '.join(sample_models[:3])}")
        
    except HttpResponseError as e:
        result["error"] = f"HTTP Error: {e.status_code} - {e.message}"
        print(f"  ✗ Not accessible - HTTP Error {e.status_code}")
    except ResourceNotFoundError as e:
        result["error"] = f"Registry not found: {str(e)}"
        print(f"  ✗ Not found")
    except Exception as e:
        result["error"] = f"Error: {type(e).__name__} - {str(e)}"
        print(f"  ✗ Error: {type(e).__name__}")
    
    return result


def discover_registries() -> List[Dict[str, Any]]:
    """
    Discover available Azure ML registries by testing known registry names.
    
    Returns:
        List of registry test results
    """
    print("=" * 60)
    print("Azure ML Registry Discovery Tool")
    print("=" * 60)
    print()
    
    # Known registry names from official Microsoft documentation and current codebase
    # Based on the image provided in the issue, these are the collections shown in the UI:
    # - Core42, DeepSeek, Meta, Microsoft, Mistral AI, OpenAI, Stability AI, xAI
    # 
    # Registry names discovered from Microsoft documentation:
    # - azureml: Main Azure ML registry (includes Microsoft/Phi models)
    # - azureml-meta: Meta/Llama models
    # - azureml-cohere: Cohere models
    # - azureml-mistral: Mistral models
    # - azureml-xai: xAI models (Grok)
    # - azureml-deepseek: DeepSeek models
    # - azureml-core42: Core42 models (Jais)
    # - azureml-stabilityai: Stability AI models (Stable Diffusion)
    # - azureml-nvidia: NVIDIA models
    # - HuggingFace: Hugging Face models
    # - azureml-gretel: Gretel models
    #
    # Note: OpenAI models appear to be in the main "azureml" registry or via Azure OpenAI service
    known_registries = [
        "azureml",              # Main Azure ML registry (Microsoft/Phi models, OpenAI, etc.)
        "azureml-meta",         # Meta/Llama models
        "azureml-cohere",       # Cohere models
        "azureml-mistral",      # Mistral models
        "azureml-xai",          # xAI models (Grok)
        "azureml-deepseek",     # DeepSeek models
        "azureml-core42",       # Core42 models (Jais - Arabic/English)
        "azureml-stabilityai",  # Stability AI models (Stable Diffusion, Stable Image)
        "azureml-nvidia",       # NVIDIA models
        "HuggingFace",          # Hugging Face models
        "azureml-gretel",       # Gretel models
        # Additional potential registries to test:
        "azureml-anthropic",    # Anthropic models (Claude) - if exists
        "azureml-google",       # Google models (Gemini) - if exists
        "azureml-ai21",         # AI21 models - if exists
        "azureml-databricks",   # Databricks models - if exists
        "azureml-openai",       # OpenAI models (separate registry) - if exists
    ]
    
    try:
        credential = DefaultAzureCredential()
        print("Successfully authenticated with Azure\n")
    except Exception as e:
        print(f"Error authenticating with Azure: {e}")
        sys.exit(1)
    
    results = []
    for registry_name in known_registries:
        result = test_registry(credential, registry_name)
        results.append(result)
        print()
    
    return results


def print_summary(results: List[Dict[str, Any]]):
    """
    Print a summary of the discovery results.
    
    Args:
        results: List of registry test results
    """
    print("=" * 60)
    print("DISCOVERY SUMMARY")
    print("=" * 60)
    print()
    
    accessible = [r for r in results if r["accessible"]]
    not_accessible = [r for r in results if not r["accessible"]]
    
    print(f"Total registries tested: {len(results)}")
    print(f"Accessible registries: {len(accessible)}")
    print(f"Not accessible registries: {len(not_accessible)}")
    print()
    
    if accessible:
        print("ACCESSIBLE REGISTRIES:")
        print("-" * 60)
        for r in accessible:
            print(f"  • {r['name']}")
            print(f"    Model count: {r['model_count']}")
            if r['sample_models']:
                print(f"    Sample models: {', '.join(r['sample_models'][:3])}")
        print()
    
    if not_accessible:
        print("NOT ACCESSIBLE REGISTRIES:")
        print("-" * 60)
        for r in not_accessible:
            print(f"  • {r['name']}")
            if r['error']:
                print(f"    Error: {r['error']}")
        print()
    
    # Generate recommended registry list
    if accessible:
        print("RECOMMENDED REGISTRY LIST FOR .env:")
        print("-" * 60)
        registry_names = ",".join([r['name'] for r in accessible])
        print(f"AZURE_ML_REGISTRY_NAMES={registry_names}")
        print()


def main():
    """Main execution function."""
    results = discover_registries()
    print_summary(results)


if __name__ == "__main__":
    main()
