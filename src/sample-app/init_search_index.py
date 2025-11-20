"""
Initialize Azure AI Search Index for LLM Poisoning Workshop

This script creates the search index with the required schema.
"""

import os
from dotenv import load_dotenv
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
)
from azure.core.credentials import AzureKeyCredential

load_dotenv()


def create_search_index():
    """Create the search index for document storage"""
    
    # Get configuration
    search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    search_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "documents-index")
    
    if not all([search_endpoint, search_key]):
        raise ValueError("Missing Azure Search configuration. Check .env file.")
    
    # Create index client
    index_client = SearchIndexClient(
        endpoint=search_endpoint,
        credential=AzureKeyCredential(search_key)
    )
    
    # Define index schema
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True
        ),
        SearchableField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
            sortable=True
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
            analyzer_name="en.microsoft"
        ),
        SearchableField(
            name="metadata",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True
        ),
    ]
    
    # Create index
    index = SearchIndex(name=index_name, fields=fields)
    
    print(f"Creating search index: {index_name}")
    
    try:
        result = index_client.create_or_update_index(index)
        print(f"✓ Index '{result.name}' created successfully")
        print(f"  Schema: {len(result.fields)} fields configured")
        for field in result.fields:
            print(f"    - {field.name} ({field.type})")
        return True
    except Exception as e:
        print(f"✗ Error creating index: {e}")
        return False


if __name__ == "__main__":
    success = create_search_index()
    exit(0 if success else 1)
