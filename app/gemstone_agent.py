"""
Gemstone Knowledge Assistant - Gemstone Agent
Executes RAG context retrieval, invokes LLM answer generation, and manages off-topic redirects.
"""

import os
from typing import Dict, Any, List

from app.rag_pipeline import retrieve
from app.config import get_api_key


class GemstoneAgent:
    """
    GemstoneAgent consumes structured output from QueryAgent, executes tool-based retrieval
    from ChromaDB, and synthesizes answers using the Groq LLM.
    """

    OFF_TOPIC_RESPONSE = (
        "I am the Gemstone Knowledge Assistant, designed specifically to answer questions "
        "about gemstones (such as Ruby, Sapphire, Moonstone, and Sri Lankan gem species, mining, and certification). "
        "I cannot answer off-topic questions. Please ask a gemstone-related query!"
    )

    def __init__(self, model_name: str = "openai/gpt-oss-120b"):
        self.model_name = model_name
        self.api_key = get_api_key("GROQ_API_KEY")
        self.llm = None

        if self.api_key:
            try:
                from langchain_groq import ChatGroq
                # Attempt initialization with requested model, fallback to llama-3.3-70b-versatile if model unavailable
                try:
                    self.llm = ChatGroq(model=self.model_name, groq_api_key=self.api_key, temperature=0.2)
                except Exception:
                    self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=self.api_key, temperature=0.2)
            except Exception:
                self.llm = None

    def process(self, query_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes query payload from QueryAgent and returns final response dictionary.
        
        Args:
            query_payload: Structured dictionary from QueryAgent.
            
        Returns:
            Dict containing answer, sources (list of filenames), and category.
        """
        category = query_payload.get("category", "off_topic")
        needs_retrieval = query_payload.get("needs_retrieval", False)
        question = query_payload.get("original_question", "")
        retrieval_query = query_payload.get("retrieval_query", question)
        k = query_payload.get("k", 4)

        # Off-topic handling (no LLM call, polite redirect)
        if category == "off_topic" or not needs_retrieval:
            return {
                "answer": self.OFF_TOPIC_RESPONSE,
                "sources": [],
                "category": "off_topic"
            }

        # Tool Call: Execute vector retrieval from ChromaDB
        retrieved_chunks = retrieve(query=retrieval_query, k=k)
        
        # Extract unique sources and combine text context
        sources = list(dict.fromkeys([chunk["source"] for chunk in retrieved_chunks if "source" in chunk]))
        context_str = "\n\n".join([
            f"--- Document Source: {chunk['source']} ---\n{chunk['content']}"
            for chunk in retrieved_chunks
        ])

        # Offline fallback synthesis if API key is not present
        if not self.llm:
            fallback_answer = (
                f"Based on reference documents ({', '.join(sources)}): "
                f"Here is the retrieved context answering '{question}':\n"
                f"{retrieved_chunks[0]['content'] if retrieved_chunks else 'No relevant context found.'}"
            )
            return {
                "answer": fallback_answer,
                "sources": sources,
                "category": category
            }

        # Prompt construction for LLM generation
        prompt = f"""You are the Gemstone Knowledge Assistant, an expert gemological AI.
Answer the user's question accurately based ONLY on the provided reference context documents.
Do not invent information. Cite key facts directly from the context.

Context Information:
{context_str}

User Question: "{question}"

Answer:"""

        try:
            response = self.llm.invoke(prompt)
            answer_text = response.content.strip()

            return {
                "answer": answer_text,
                "sources": sources,
                "category": category
            }

        except Exception as e:
            # Fallback if API fails during generation
            fallback_answer = (
                f"Retrieved Context ({', '.join(sources)}):\n"
                f"{retrieved_chunks[0]['content'] if retrieved_chunks else 'No context retrieved.'}"
            )
            return {
                "answer": fallback_answer,
                "sources": sources,
                "category": category
            }
