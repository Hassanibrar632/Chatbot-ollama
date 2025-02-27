# Chatbot-Ollama - Full System Overview

This repository contains both the **Backend** and **Frontend** components of a chatbot system powered by Ollama. The system allows users to upload files, manage indexes, and interact with a chatbot using a Streamlit-based interface.

## Features
- **File Upload & Index Creation**: Upload multiple files and create searchable indexes.
- **List & Manage Indexes**: Retrieve, select, and delete available indexes.
- **Interactive Chatbot**: Query indexed data using a conversational chatbot.

## Project Structure
```
Chatbot-Ollama/
│── Backend/            # Contains backend API logic
│── Frontend/           # Streamlit-based frontend UI
│── .env                # Environment variables (API keys, secrets, etc.)
│── .gitattributes      # Git configuration
│── .gitignore         # Git ignore file
│── LICENSE            # License file
│── README.md          # Documentation
│── requirements.txt   # Dependencies for the project
│── run_backend.bat    # Windows batch file to start the backend
│── run_frontend.bat   # Windows batch file to start the frontend
│── setup.bat          # Windows batch file for setup
```

## Setting Up Environment Variables
Create a `.env` file in the root directory and add the following:
```
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
```
Ensure that this file is not shared publicly as it contains sensitive credentials.

## Setup Instructions
### **1. Install Dependencies**
Ensure you have Conda installed, then run:
```bash
setup.bat
```
This script will:
- Create a Conda environment named `llm`.
- Install required dependencies.
- Pull the latest `llama3.2` model using Ollama.

### **2. Run the Backend**
To start the backend API server:
```bash
run_backend.bat
```
This script will activate the `llm` environment and run the backend API (`Backend/api.py`).

### **3. Run the Frontend**
To start the frontend UI:
```bash
run_frontend.bat
```
This script will activate the `llm` environment and launch the Streamlit application (`Frontend/App.py`).

## API Endpoints
| Method  | Endpoint              | Description                        |
|---------|-----------------------|------------------------------------|
| POST    | `/upload/`            | Uploads files and creates an index. |
| GET     | `/list/`              | Retrieves the list of created indexes. |
| DELETE  | `/delete/{index_id}`  | Deletes an index. |
| POST    | `/chat/{index_id}`    | Sends a query to the chatbot and retrieves a response. |

## Calling API Endpoints via `requests`
Here’s how you can interact with the backend API using Python’s `requests` module:

### **Upload Files**
```python
import requests

files = {'files': open('sample.txt', 'rb')}
response = requests.post("http://127.0.0.1:8000/upload/", files=files)
print(response.json())
```

### **List Available Indexes**
```python
response = requests.get("http://127.0.0.1:8000/list/")
print(response.json())
```

### **Delete an Index**
```python
index_id = "your_index_id"
response = requests.delete(f"http://127.0.0.1:8000/delete/{index_id}")
print(response.json())
```

### **Chat with the Chatbot**
```python
index_id = "your_index_id"
data = {"query": "Hello, how does this work?"}
response = requests.post(f"http://127.0.0.1:8000/chat/{index_id}", json=data)
print(response.json())
```

## Notes
- Ensure the backend is running before using the frontend.
- The chatbot responses are streamed for a smoother user experience.

