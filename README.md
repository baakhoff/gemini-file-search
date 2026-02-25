# gemini-file-search

I wanted to use Gemini File Search as a RAG (Retrieval-Augmented Generation) system and found no simple code examples on it, so I decided to make my own. 

This repository provides reusable helper functions to easily intractable with the Google Gemini File Search API directly from your Python scripts or Jupyter Notebooks.

## Features

- **Store Management**: Create, list, and delete Gemini File Search Stores.
- **File Management**: Upload documents directly into a Store with optional metadata and delete documents.
- **Document Querying**: Query the uploaded documents within a store using the Gemini model (defaults to `gemini-2.5-flash`).

## Prerequisites

1.  **Python 3.13** (or a compatible modern Python 3 version)
2.  **A Google Gemini API Key**. You can get one from Google AI Studio.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/baakhoff/gemini-file-search.git
    cd gemini-file-search
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    Create a `.env` file in the root directory and add your API Key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## Usage

The core interaction logic is inside `gemini_file_search.py`. This script provides a set of helper functions that you can import and use via Python scripts or Jupyter notebooks.

### Direct Script Usage Example

You can import and use the functionality anywhere:

```python
import gemini_file_search as gfs

# 1. Get the authenticated client
client = gfs.get_client()

# 2. Create a specific file search store
store = gfs.create_file_search_store(client, "My Document Store")

# 3. Upload a document (e.g., 'resume.pdf' or 'data.txt')
gfs.upload_file_to_store(client, "path/to/my_document.txt", store.name)

# 4. Query the documents in the store
response = gfs.query_file_search_store(
    client, 
    store.name, 
    query="Summarize the main points of the uploaded document."
)
print(response.text)

# 5. Cleanup
gfs.delete_file_search_store(client, store.name)
```

## Available Helper Functions

In `gemini_file_search.py`:

*   `get_client() -> genai.Client`
*   `create_file_search_store(client, display_name) -> Store`
*   `list_file_search_stores(client) -> List[Store]`
*   `delete_file_search_store(client, store_name, force=True)`
*   `upload_file_to_store(client, file_path, store_name, display_name=None, metadata=None) -> Operation`
*   `list_documents_in_store(client, store_name) -> List[Document]`
*   `delete_document_from_store(client, document_name)`
*   `query_file_search_store(client, store_name, query, metadata_filter=None, model="gemini-2.5-flash") -> Response`
