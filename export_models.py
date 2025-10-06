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

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from dotenv import load_dotenv


def get_project_client() -> AIProjectClient:
    """
    Create and return an AIProjectClient for accessing Azure AI Foundry.
    
    Returns:
        AIProjectClient: Configured AI Project client
    """
    load_dotenv()
    
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    
    if not project_endpoint:
        print("Error: Missing required environment variable.")
        print("Please set PROJECT_ENDPOINT")
        print("You can copy .env.example to .env and fill in your values.")
        sys.exit(1)
    
    try:
        credential = DefaultAzureCredential()
        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=credential
        )
        return project_client
    except Exception as e:
        print(f"Error creating AI Project client: {e}")
        sys.exit(1)


def fetch_models(project_client: AIProjectClient) -> List[Dict[str, Any]]:
    """
    Fetch all deployed models from the AI Foundry project.
    
    Args:
        project_client: The AIProjectClient instance
        
    Returns:
        List of model dictionaries with their details
    """
    print("Fetching deployed models from AI Foundry project...")
    models_data = []
    
    try:
        deployments = project_client.deployments.list()
        
        for deployment in deployments:
            model_info = {
                "Name": deployment.name,
                "Model Name": deployment.model_name if hasattr(deployment, 'model_name') else "N/A",
                "Model Version": deployment.model_version if hasattr(deployment, 'model_version') else "N/A",
                "Model Publisher": deployment.model_publisher if hasattr(deployment, 'model_publisher') else "N/A",
                "Type": deployment.type if hasattr(deployment, 'type') else "N/A",
                "SKU": str(deployment.sku) if hasattr(deployment, 'sku') else "N/A",
                "Capabilities": ", ".join(deployment.capabilities) if hasattr(deployment, 'capabilities') and deployment.capabilities else "N/A",
                "Connection": deployment.connection_name if hasattr(deployment, 'connection_name') else "N/A",
            }
            models_data.append(model_info)
            
        print(f"Found {len(models_data)} deployed models")
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
    headers = ["Name", "Model Name", "Model Version", "Model Publisher", "Type", "SKU", "Capabilities", "Connection"]
    
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
            except (TypeError, AttributeError):
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
    
    # Get AI Project client
    project_client = get_project_client()
    
    # Fetch models
    models_data = fetch_models(project_client)
    
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
