# Libraries to enable user to sue chatbot and get responses
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core.node_parser.text import SentenceSplitter
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.ollama import Ollama
import tqdm

# Libraries for the API developement
from pinecone import Pinecone
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import shutil
import uuid
import os

# Load the .env file to use that for API calling
load_dotenv()

app = Flask(__name__)

# Uploading Dir where we will save the files
UPLOAD_DIR = "Backend/uploads"

# Get Pinecone API Key
api = os.getenv('PC_API')

# Setting the params for the llama-index
Settings.transformations = [SentenceSplitter(chunk_size=1024, chunk_overlap=512)]
Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = Ollama(model="llama3.2:latest", request_timeout=600)

# Initilize a chategine to change and use it globally
chat_engine = None                          # chat engine to use it globally
cur_index = None                            # cur_index to check if the request is from another index or not

# helper Function to load the requested Index
def load_chatbot_by_index(index_id):
    # load pinecone index that is requested
    pc = Pinecone(api_key=api)
    pinecone_index = pc.Index(index_id)
    
    # load your index from stored vectorspace
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )

    # get the gloabl chat_engine
    global chat_engine
    chat_engine = index.as_chat_engine(                                             # create a chat engine using the requested index
        chat_mode="condense_plus_context",                                          # set the engine mode
        memory=ChatMemoryBuffer.from_defaults(token_limit=3900),                    # set the memeory to save its previous chats
        similarity_top_k=5
    )
    # index.as_query_engine()

    # laod the global cur_index and change its value to the requested index_id
    global cur_index
    cur_index = index_id

    print(f"{'='*30}\nCreated Chat_Engine\n{'='*30}")
    return True


@app.route("/upload/", methods=["POST"])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided."}), 400

        files = request.files.getlist("files")
        print(f"Received {len(files)} files:")
        for f in files:
            print(f.filename)

        # Generate a unique folder name
        folder_name = str(uuid.uuid4())
        folder_path = Path(UPLOAD_DIR) / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        
        file_details = []
        for file in files:
            file_path = folder_path / file.filename
            file.save(file_path)
            file_details.append({"filename": file.filename, "path": str(file_path)})
        
        # Start a subprocess to execute a script with sleep_time as argument
        script_path = Path("Backend/Preprocess.py").absolute()
        subprocess.Popen(["python", str(script_path), folder_name], shell=True)

        return jsonify({"folder": folder_name, "file_count": len(files), "files": file_details})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/list/", methods=["GET"])
def get_indexces():
    try:
        pc = Pinecone(api_key=api)
        index_list = pc.list_indexes()                          # Get the indexces list
        index_ls = [index["name"] for index in index_list]      # Extracting only index names

        return jsonify({"index_names": index_ls})                # return the indexces names list
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/delete/<index_id>", methods=["DELETE"])
def delete_index(index_id):
    try:
        pc = Pinecone(api_key=api)
        
        # Check if the index is created
        if pc.has_index(index_id):
            # delete the index
            pc.delete_index(index_id)

        folder_path = Path(UPLOAD_DIR) / index_id  # Change this to the folder you want to delete
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({"Message": f'Index Deleted {index_id}'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat/<index_id>", methods=["POST"])
def chat_bot(index_id):
    data = request.get_json()
    query_text = data.get("query") if data else None
    if not query_text:
        return jsonify({"error": "No query provided"}), 400
    print(f"{'='*30}\n{query_text}\n{'='*30}")
    
    if index_id != cur_index:
        print(f"{'='*30}\nChanging the index\n{'='*30}")
        load_chatbot_by_index(index_id=index_id)
    global chat_engine
    response = chat_engine.chat(query_text)

    print(f"{'='*30}\n{response}\n{'='*30}")
    
    # Return the response that is generated by the chatbot
    return jsonify({"text": str(response)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
