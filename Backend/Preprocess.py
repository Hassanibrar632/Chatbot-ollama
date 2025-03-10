from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core.node_parser.text import SentenceSplitter
from pinecone import Pinecone, ServerlessSpec
from llama_index.core.schema import TextNode
from dotenv import load_dotenv
from pathlib import Path
import tqdm
import sys
import os

# Load the .env file to use that for API calling
load_dotenv()

# Get Pinecone API Key
api = os.getenv('pinecone_api')


def get_nodes(folder_path):

    print(os.listdir(folder_path))
    
    # craete a sentence Splitter to split the documents into sentences with chunk size and overlap to capture a part of the previous sentence
    text_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=512)

    """
    Following steps are taking place in the following function:

    1. Extract the documents data and make overlaping chunks from the docs.
    2. Create the text nodes to add meta data to the nodes.
    3. Embed the nodes for vector spaces and to use RAG models on it.
    4. Return the Embedded nodes for further preprocessing. 
    """
    
    text_chunks = []                # This will hold all the chunks of text from all documents
    doc_idxs = []                   # This will keep track of the document each chunk came from
    docs = SimpleDirectoryReader(folder_path).load_data()

    for doc_idx, doc in enumerate(docs):
        # Split the current document's text into chunks
        cur_text_chunks = text_parser.split_text(doc.text)
        # Extend the list of all text chunks with the chunks from the current document
        text_chunks.extend(cur_text_chunks)
        # Extend the document index list with the index of the current document, repeated for each chunk
        doc_idxs.extend([doc_idx] * len(cur_text_chunks))

    nodes = []                          # This will hold all TextNode objects created from the text chunks
    # Iterate over each text chunk and its index
    for idx, text_chunk in tqdm.tqdm(enumerate(text_chunks)):
        node = TextNode(text=text_chunk)    # Create a TextNode object with the current text chunk
        src_doc = docs[doc_idxs[idx]]       # Retrieve the source document using the current index mapped through doc_idxs
        node.metadata = src_doc.metadata    # Assign the source document's metadata to the node's metadata attribute
        nodes.append(node)                  # Append the newly created node to the list of nodes

    embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
    for node in tqdm.tqdm(nodes):
        node_embedding = embed_model.get_text_embedding(node.get_content(metadata_mode="all"))
        node.embedding = node_embedding
    
    return nodes, embed_model


def get_pinecone_store(folder_name, dim):
    """
    Create the pinecone index for the folder that is being processed.
    then create the vector store for the llamaindex to store the embeddings.
    """

    # Create Pinecone Vector Store
    pc = Pinecone(api_key=api)

    # Check if the index is already creted
    if pc.has_index(folder_name):
        pc.delete_index(folder_name)                                # Delete the initial index
        print(f"{'='*10} Previous Index Removed {'='*10}")

    pc.create_index(                                                # Create a new Index with the same name as of folder
        name=folder_name,
        dimension=dim,                                              # dim of the embedded text
        metric="dotproduct",                                        # This metric was used to train the model so using this
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),       # Straight from pinecone documentation other regions locked
    )
    print(f"{'='*10} New Index Created {'='*10}")

    pinecone_index = pc.Index(folder_name)                          # get the index where we will store the data

    vector_store = PineconeVectorStore(                             # create vector store to save embeddings using llamaindex
        pinecone_index=pinecone_index,                              # use the index that is creted using the folder
    )

    return vector_store

def store_index(nodes, storage_context, transformations):
    # Upsert vectors into the pinecone index
    _ = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        transformations=transformations,
    )

    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python delayed_script.py <sleep_time>")
        sys.exit(1)
    
    try:
        folder_name = str(sys.argv[1])
        folder_path = str(Path(f"Backend/uploads/{folder_name}").absolute()).replace('\\', '/')
    except ValueError:
        print("Invalid Folder path. Please provide valid folder path.")
        sys.exit(1)

    nodes, embed_model = get_nodes(folder_path=folder_path)                                  # get nodes of the documents
    dim = len(nodes[0].embedding)                                               # calculate dim
    vector_store = get_pinecone_store(folder_name=folder_name, dim=dim)         # get pinecone vectore store

    # Setup the paramters for the upserting process of the vectore to the vector spcae
    Settings.embed_model = embed_model
    transformations = [SentenceSplitter(chunk_size=1024, chunk_overlap=512)]
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # store the indexes
    if store_index(nodes=nodes, storage_context=storage_context, transformations=transformations):
        print(f"{'='*10} vectors stored {'='*10}")
    else:
        print(f"{'='*10} Process Failed {'='*10}")

if __name__ == "__main__":
    main()