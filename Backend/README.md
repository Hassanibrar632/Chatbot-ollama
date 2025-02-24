# Backend for Chatbot with Pinecone and LlamaIndex

## Overview
This backend provides an API for uploading documents, processing them into vector embeddings using Pinecone and LlamaIndex, and enabling chatbot interactions based on stored embeddings.

## Features
- **Document Upload**: Uploads and processes documents into vector embeddings.
- **Vector Storage**: Uses Pinecone for efficient vector-based retrieval.
- **Chatbot Interface**: Provides conversational responses using LlamaIndex and Ollama.
- **Index Management**: Lists, loads, and deletes vector indices.

## Technologies Used
- **Python**
- **Flask** (for API development)
- **LlamaIndex** (for text embedding and retrieval)
- **Pinecone** (vector database for storing embeddings)
- **FastEmbed** (text embedding model: `BAAI/bge-small-en-v1.5`)
- **Ollama** (LLM for chatbot responses)
- **TQDM** (progress tracking)
- **Dotenv** (environment variable management)

---

## Project Structure
```
Backend/
│── uploads/                # Stores uploaded documents temporarily
│── Preprocess.py           # Handles text preprocessing and vector storage
│── api.py                  # Flask API for document handling and chatbot interaction
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repo_url>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Pinecone API key:
   ```
   PC_API=your_pinecone_api_key
   ```

---

## Usage

### Start the API Server
```bash
python api.py
```
This starts the Flask API on `http://0.0.0.0:8000`.

### API Endpoints

#### 1. Upload Documents
- **Endpoint**: `POST /upload/`
- **Description**: Uploads files and processes them into vector embeddings.
- **Payload**: Multipart form-data with `files`.
- **Response**:
  ```json
  {
    "folder": "<generated_folder_id>",
    "file_count": 2,
    "files": [
      {"filename": "example.txt", "path": "Backend/uploads/<folder_id>/example.txt"}
    ]
  }
  ```

#### 2. List Available Indices
- **Endpoint**: `GET /list/`
- **Response**:
  ```json
  {
    "index_names": ["index_1", "index_2"]
  }
  ```

#### 3. Delete an Index
- **Endpoint**: `DELETE /delete/<index_id>`
- **Response**:
  ```json
  {
    "Message": "Index Deleted <index_id>"
  }
  ```

#### 4. Chatbot Interaction
- **Endpoint**: `POST /chat/<index_id>`
- **Payload**:
  ```json
  {
    "query": "What is AI?"
  }
  ```
- **Response**:
  ```json
  {
    "text": "AI stands for Artificial Intelligence..."
  }
  ```

---

## How It Works
### **Preprocessing (`Preprocess.py`)**
1. Reads documents from the uploaded folder.
2. Splits text into overlapping chunks.
3. Creates text nodes with metadata.
4. Embeds text using FastEmbed (`bge-small-en-v1.5`).
5. Stores embeddings in Pinecone for retrieval.

### **API Server (`api.py`)**
1. Handles file uploads and triggers preprocessing.
2. Manages Pinecone indices (list, delete).
3. Loads chatbot instance dynamically based on requested index.
4. Uses LlamaIndex with Ollama to generate chatbot responses.

---

## Future Enhancements
- Add support for additional embedding models.
- Implement authentication and access control.
- Expand chatbot memory beyond session-based interactions.

---

## License
MIT License

