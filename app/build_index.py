"""
Gemstone Knowledge Assistant - Index Builder Script
One-time script to chunk documents, generate embeddings, and populate persistent ChromaDB collection.
"""

import sys
import os

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.rag_pipeline import index_documents, CHROMA_DB_DIR


def main():
    print("=" * 60)
    print("[INFO] Starting Gemstone Knowledge Base indexing process...")
    print("=" * 60)

    try:
        total_chunks = index_documents()
        print(f"[SUCCESS] Successfully indexed {total_chunks} document chunks.")
        print(f"[INFO] Vector database stored at: {CHROMA_DB_DIR}")
        print("=" * 60)

    except Exception as e:
        print(f"[ERROR] Indexing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
