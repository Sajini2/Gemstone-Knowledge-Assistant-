"""
Gemstone Knowledge Assistant - Agent 3: RetrievalAgent
Task: Vector Store Lookup, Chunk Retrieval, and Source Context Extraction.
"""

import sys
import os
from typing import Dict, Any, List

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.rag_pipeline import retrieve


class RetrievalAgent:
    """
    Agent 3: RetrievalAgent
    Executes tool-based vector search against persistent ChromaDB vector store.
    """

    def process(self, planner_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves matching document chunks from ChromaDB.
        
        Args:
            planner_payload: Output dict from PlannerAgent.
            
        Returns:
            Dict: {original_question, category, is_off_topic, chunks, sources}
        """
        question = planner_payload.get("original_question", "")
        category = planner_payload.get("category", "off_topic")
        is_off_topic = planner_payload.get("is_off_topic", True)
        retrieval_query = planner_payload.get("retrieval_query", question)
        k = planner_payload.get("k", 4)

        if is_off_topic or category == "off_topic" or k == 0:
            return {
                "original_question": question,
                "category": "off_topic",
                "is_off_topic": True,
                "chunks": [],
                "sources": []
            }

        # Tool Call: Vector Search against ChromaDB
        retrieved_chunks = retrieve(query=retrieval_query, k=k)
        
        # Deduplicate source document filenames
        sources = list(dict.fromkeys([chunk["source"] for chunk in retrieved_chunks if "source" in chunk]))

        return {
            "original_question": question,
            "category": category,
            "is_off_topic": False,
            "chunks": retrieved_chunks,
            "sources": sources
        }
