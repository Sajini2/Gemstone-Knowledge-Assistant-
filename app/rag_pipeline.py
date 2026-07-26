"""
Gemstone Knowledge Assistant - RAG Pipeline Module
Handles document loading, chunking, embedding generation, ChromaDB vector persistence, and retrieval.
"""

import sys
import os
import site

# Ensure User Site Packages directory is first in sys.path for onnxruntime & chromadb
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.insert(0, user_site)

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
    """
    Returns local embedding function with robust fallbacks:
    1. SentenceTransformerEmbeddingFunction ("all-MiniLM-L6-v2")
    2. ONNXMiniLM_L6_V2
    3. DefaultEmbeddingFunction (ChromaDB Built-in)
    """
    try:
        return embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    except Exception:
        pass

    try:
        return embedding_functions.ONNXMiniLM_L6_V2()
    except Exception:
        pass

    return embedding_functions.DefaultEmbeddingFunction()


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

        for idx, chunk_text in enumerate(chunks):
            chunk_counter += 1
            chunk_id = f"doc_{filename}_chunk_{idx+1}"
            
            documents.append(chunk_text)
            metadatas.append({
                "source": filename,
                "chunk_index": idx + 1,
                "total_chunks": len(chunks)
            })
            ids.append(chunk_id)

    return documents, metadatas, ids


def build_vector_store() -> int:
    """
    Chunks all documents in documents/ and populates ChromaDB persistent collection.
    
    Returns:
        Int count of indexed document chunks.
    """
    documents, metadatas, ids = load_and_chunk_documents()
    client = get_chroma_client()
    ef = get_embedding_function()

    # Get or create collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"description": "Gemstone domain knowledge base chunks"}
    )

    # Upsert chunks in batches
    batch_size = 50
    for i in range(0, len(documents), batch_size):
        end_idx = min(i + batch_size, len(documents))
        collection.upsert(
            documents=documents[i:end_idx],
            metadatas=metadatas[i:end_idx],
            ids=ids[i:end_idx]
        )

    return collection.count()


# Alias for backwards compatibility
index_documents = build_vector_store


def retrieve(query: str, k: int = 4) -> List[Dict[str, Any]]:
    """
    Retrieves top-k most relevant document chunks for a query from ChromaDB.
    
    Args:
        query: User or rephrased search query string.
        k: Number of top chunks to retrieve (default: 4).
        
    Returns:
        List of dicts: [{content, source, chunk_index, distance}]
    """
    client = get_chroma_client()
    ef = get_embedding_function()

    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )
        results = collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
    except Exception as e:
        # If collection doesn't exist, build vector index on the fly
        build_vector_store()
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )
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
