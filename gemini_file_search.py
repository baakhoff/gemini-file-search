import os
import time
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_client() -> genai.Client:
    """Initializes and returns the GenAI client using the environment variable GEMINI_API_KEY."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in your .env file.")
    return genai.Client()

def create_file_search_store(client: genai.Client, display_name: str):
    """Creates a new File Search Store."""
    store = client.file_search_stores.create(config={'display_name': display_name})
    print(f"Created File Search Store: {store.name} (Display Name: {store.display_name})")
    return store

def list_file_search_stores(client: genai.Client):
    """Lists all available File Search Stores."""
    stores = list(client.file_search_stores.list())
    print(f"Found {len(stores)} File Search Store(s).")
    for store in stores:
         print(f" - {store.name} (Display Name: {store.display_name})")
    return stores

def delete_file_search_store(client: genai.Client, store_name: str, force: bool = True):
    """Deletes a File Search Store by its name."""
    client.file_search_stores.delete(name=store_name, config={'force': force})
    print(f"Deleted File Search Store: {store_name}")

def upload_file_to_store(client: genai.Client, file_path: str, store_name: str, display_name: Optional[str] = None, metadata: Optional[List[Dict[str, Any]]] = None):
    """Uploads a local file and imports it into a File Search Store."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    config = {}
    if display_name:
        config['display_name'] = display_name
    if metadata:
        config['custom_metadata'] = metadata

    print(f"Uploading and importing {file_path} to store {store_name}...")
    operation = client.file_search_stores.upload_to_file_search_store(
        file=file_path,
        file_search_store_name=store_name,
        config=config if config else None
    )
    
    # Wait for the operation to complete
    print("Waiting for upload and indexing to complete...")
    while not operation.done:
        time.sleep(5)
        operation = client.operations.get(operation)
        print(".", end="", flush=True)
    print("\nUpload and import complete.")
    return operation

def list_documents_in_store(client: genai.Client, store_name: str):
    """Lists all documents within a specific File Search Store."""
    documents = list(client.file_search_stores.documents.list(parent=store_name))
    print(f"Found {len(documents)} document(s) in store {store_name}.")
    for doc in documents:
        print(f" - Document Name: {doc.name}")
    return documents

def delete_document_from_store(client: genai.Client, document_name: str):
    """Deletes a specific document from a File Search Store."""
    client.file_search_stores.documents.delete(name=document_name)
    print(f"Deleted document: {document_name}")

def query_file_search_store(client: genai.Client, store_name: str, query: str, metadata_filter: Optional[str] = None, model: str = "gemini-2.5-flash"):
    """Queries the model using the contents of a File Search Store."""
    print(f"Querying model '{model}' with File Search Store '{store_name}'...")
    
    file_search_config = types.FileSearch(file_search_store_names=[store_name])
    if metadata_filter:
        file_search_config.metadata_filter = metadata_filter
        
    tool = types.Tool(file_search=file_search_config)
    
    response = client.models.generate_content(
        model=model,
        contents=query,
        config=types.GenerateContentConfig(tools=[tool])
    )
    return response

if __name__ == "__main__":
    print("This file now contains helper functions for the Gemini File Search API.")
    print("Please import these functions in your notebook (e.g., test.ipynb) to use them.")
