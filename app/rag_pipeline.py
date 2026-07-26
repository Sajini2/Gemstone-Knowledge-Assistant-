"""
Gemstone Knowledge Assistant - RAG Pipeline Module
Handles document loading, chunking, embedding generation, ChromaDB vector persistence, and retrieval.
"""

import os
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "gemstone_knowledge_base"


def get_embedding_function():
    """Returns local ONNX all-MiniLM-L6-v2 embedding function (no API cost)."""
    return embedding_functions.ONNXMiniLM_L6_V2()


def get_chroma_client():
    """Returns persistent ChromaDB client pointing to local ./chroma_db directory."""
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)


def load_and_chunk_documents() -> tuple[List[str], List[Dict[str, Any]], List[str]]:
    """
    Loads all .txt documents from documents/ directory and splits them into chunks.
    Uses RecursiveCharacterTextSplitter with chunk_size=400 and chunk_overlap=50.
    
    Returns:
        tuple of (chunk_texts, metadata_list, chunk_ids)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    documents = []
    metadatas = []
    ids = []

    if not os.path.exists(DOCUMENTS_DIR):
        raise FileNotFoundError(f"Documents directory not found at: {DOCUMENTS_DIR}")

    files = sorted([f for f in os.listdir(DOCUMENTS_DIR) if f.endswith(".txt")])

    chunk_counter = 0
    for filename in files:
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()

        chunks = splitter.split_text(text)
        for idx, chunk in enumerate(chunks):
            chunk_counter += 1
            documents.append(chunk)
            metadatas.append({"source": filename, "chunk_index": idx})
            ids.append(f"{filename}_chunk_{idx}")

    return documents, metadatas, ids


def build_or_get_index():
    """Populates ChromaDB with document chunks if collection is empty or creates index."""
    client = get_chroma_client()
    ef = get_embedding_function()
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )
    
    return collection


def index_documents():
    """Executes document loading, chunking, and persists vectors to ChromaDB."""
    client = get_chroma_client()
    ef = get_embedding_function()
    
    # Reset/recreate collection for fresh indexing
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    documents, metadatas, ids = load_and_chunk_documents()
    
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    return len(documents)


def retrieve(query: str, k: int = 4) -> List[Dict[str, Any]]:
    """
    Retrieves the top-k most relevant text chunks from ChromaDB for a given query.
    
    Args:
        query: Search query string.
        k: Number of relevant chunks to retrieve (default: 4).
        
    Returns:
        List of dictionaries containing 'content', 'source', and 'distance'.
    """
    client = get_chroma_client()
    ef = get_embedding_function()
    
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )
    except Exception as e:
        raise RuntimeError(
            "ChromaDB collection not found. Please run 'python app/build_index.py' first."
        ) from e

    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    retrieved_chunks = []
    if results and results.get("documents") and len(results["documents"]) > 0:
        docs = results["documents"][0]
        meta = results["metadatas"][0]
        dists = results["distances"][0] if "distances" in results else [0.0] * len(docs)

        for doc, metadata, dist in zip(docs, meta, dists):
            retrieved_chunks.append({
                "content": doc,
                "source": metadata.get("source", "unknown"),
                "chunk_index": metadata.get("chunk_index", 0),
                "distance": float(dist)
            })

    return retrieved_chunks
