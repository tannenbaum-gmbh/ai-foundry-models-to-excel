#!/usr/bin/env python3
"""
Export AI Foundry Model Catalog to Excel

This script fetches all available models from Azure AI Foundry (Model Catalog)
and exports them to an Excel file with details about each model.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from dotenv import load_dotenv


def get_ml_client() -> MLClient:
    """
    Create and return an MLClient for accessing Azure AI Foundry.
    
    Returns:
        MLClient: Configured ML client
    """
    load_dotenv()
    
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    workspace_name = os.getenv("AZURE_WORKSPACE_NAME")
    
    if not all([subscription_id, resource_group, workspace_name]):
        print("Error: Missing required environment variables.")
        print("Please set AZURE_SUBSCRIPTION_ID, AZURE_RESOURCE_GROUP, and AZURE_WORKSPACE_NAME")
        print("You can copy .env.example to .env and fill in your values.")
        sys.exit(1)
    
    try:
        credential = DefaultAzureCredential()
        ml_client = MLClient(
            credential=credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
        return ml_client
    except Exception as e:
        print(f"Error creating ML client: {e}")
        sys.exit(1)


def fetch_models(ml_client: MLClient) -> List[Dict[str, Any]]:
    """
    Fetch all models from the AI Foundry catalog.
    
    Args:
        ml_client: The MLClient instance
        
    Returns:
        List of model dictionaries with their details
    """
    print("Fetching models from AI Foundry catalog...")
    models_data = []
    
    try:
        models = ml_client.models.list()
        
        for model in models:
            model_info = {
                "Name": model.name,
                "Version": model.version,
                "Description": model.description or "N/A",
                "Tags": ", ".join([f"{k}:{v}" for k, v in (model.tags or {}).items()]),
                "Type": model.type or "N/A",
                "Path": model.path or "N/A",
                "Created Date": model.creation_context.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(model, 'creation_context') and model.creation_context else "N/A",
                "Created By": model.creation_context.created_by if hasattr(model, 'creation_context') and model.creation_context else "N/A",
            }
            models_data.append(model_info)
            
        print(f"Found {len(models_data)} models")
        return models_data
        
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def export_to_excel(models_data: List[Dict[str, Any]], output_file: str):
    """
    Export models data to an Excel file with formatting.
    
    Args:
        models_data: List of model dictionaries
        output_file: Path to output Excel file
    """
    print(f"Exporting {len(models_data)} models to Excel...")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "AI Foundry Models"
    
    # Define headers
    headers = ["Name", "Version", "Description", "Tags", "Type", "Path", "Created Date", "Created By"]
    
    # Style for headers
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    # Write headers
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    # Write data
    for row_num, model in enumerate(models_data, 2):
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = model.get(header, "N/A")
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    
    # Auto-adjust column widths
    for col_num in range(1, len(headers) + 1):
        column_letter = get_column_letter(col_num)
        max_length = 0
        for cell in ws[column_letter]:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Freeze the header row
    ws.freeze_panes = "A2"
    
    # Save the workbook
    wb.save(output_file)
    print(f"Excel file saved to: {output_file}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("AI Foundry Models to Excel Exporter")
    print("=" * 60)
    print()
    
    # Get ML client
    ml_client = get_ml_client()
    
    # Fetch models
    models_data = fetch_models(ml_client)
    
    if not models_data:
        print("No models found or error occurred.")
        sys.exit(1)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"ai_foundry_models_{timestamp}.xlsx"
    
    # Export to Excel
    export_to_excel(models_data, output_file)
    
    print()
    print("=" * 60)
    print("Export completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
