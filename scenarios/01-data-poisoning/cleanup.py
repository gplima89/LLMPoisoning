"""
Cleanup script to remove poisoned documents from Azure AI Search
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/sample-app'))

from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()


def cleanup_poisoned_documents():
    """Remove poisoned documents and restore clean state"""
    
    print("=" * 70)
    print("CLEANUP - REMOVING POISONED DOCUMENTS")
    print("=" * 70)
    print()
    
    # Get configuration
    search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    search_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "documents-index")
    
    # Create search client
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_key)
    )
    
    # IDs of poisoned documents to remove
    poisoned_doc_ids = [
        "sec-policy-2024-update",
        "mfa-service-notice-2024",
        "collab-best-practices-2024"
    ]
    
    print(f"Removing {len(poisoned_doc_ids)} poisoned documents...")
    print()
    
    # Delete each poisoned document
    for doc_id in poisoned_doc_ids:
        try:
            # Search for the document first to verify it exists
            results = list(search_client.search(
                search_text="*",
                filter=f"id eq '{doc_id}'",
                select="id,title"
            ))
            
            if results:
                doc = results[0]
                print(f"  Found: {doc['title']}")
                
                # Delete the document
                search_client.delete_documents(documents=[{"id": doc_id}])
                print(f"  ✓ Deleted: {doc_id}")
            else:
                print(f"  ℹ Not found: {doc_id} (may already be deleted)")
            
        except Exception as e:
            print(f"  ✗ Error deleting {doc_id}: {e}")
    
    print()
    
    # Verify cleanup
    print("Verifying cleanup...")
    remaining_count = search_client.get_document_count()
    print(f"  Documents remaining in index: {remaining_count}")
    
    # Check if any poisoned docs still exist
    still_poisoned = False
    for doc_id in poisoned_doc_ids:
        results = list(search_client.search(
            search_text="*",
            filter=f"id eq '{doc_id}'",
            select="id"
        ))
        if results:
            still_poisoned = True
            print(f"  ⚠ Warning: {doc_id} still exists")
    
    print()
    print("=" * 70)
    
    if not still_poisoned:
        print("✓ CLEANUP COMPLETE")
        print()
        print("All poisoned documents have been removed.")
        print("The system should now return to baseline behavior.")
        print()
        print("Next steps:")
        print("1. Run test_before_poisoning.py to verify clean state")
        print("2. Review logs for any suspicious activity")
        print("3. Document lessons learned")
    else:
        print("✗ CLEANUP INCOMPLETE")
        print()
        print("Some poisoned documents may still exist.")
        print("Manual intervention may be required.")
    
    print("=" * 70)


if __name__ == "__main__":
    cleanup_poisoned_documents()
