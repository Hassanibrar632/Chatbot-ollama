# Frontend - File Uploader & Chatbot Interface

This frontend application provides a user-friendly interface for uploading files, managing indexes, and interacting with a chatbot using Streamlit.

## Features
- Upload files to create indexes
- List available indexes for retrieval-augmented generation (RAG)
- Select and delete indexes
- Chatbot interface for querying indexed data

## Requirements
Ensure you have Python installed and install dependencies using:
```bash
pip install streamlit requests
```

## Running the Application
To start the frontend, run:
```bash
streamlit run App.py
```

## Functionality Breakdown
### **1. Create Index (Upload Files)**
- Allows users to upload multiple files.
- Sends files to the backend API (`/upload/`).
- Displays success messages upon completion.

### **2. List Indexes**
- Fetches available indexes from the backend (`/list/`).
- Allows users to select an index for chatbot usage or delete an index.

### **3. Chatbot**
- Users can select an index for querying.
- Sends user input to the backend chatbot API (`/chat/{index_id}`).
- Displays streamed responses from the chatbot.

## API Endpoints Used
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

