"""
Gemstone Knowledge Assistant - Agent 4: SynthesizerAgent
Task: RAG Response Synthesis, Factual Grounding, and Off-Topic Filtering.
Supports Groq API and OpenRouter API providers.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from typing import Dict, Any, List
from app.config import get_api_key


class SynthesizerAgent:
    """
    Agent 4: SynthesizerAgent
    Consumes retrieved context chunks from RetrievalAgent and synthesizes source-grounded answers.
    Supports Groq and OpenRouter LLMs.
    """

    OFF_TOPIC_RESPONSE = (
        "I am the Gemstone Knowledge Assistant, designed specifically to answer questions "
        "about gemstones (such as Ruby, Sapphire, Moonstone, and Sri Lankan gem species, mining, and certification). "
        "I cannot answer off-topic questions. Please ask a gemstone-related query!"
    )

    def __init__(self, groq_model: str = "openai/gpt-oss-120b", openrouter_model: str = "openai/gpt-4o-mini"):
        self.groq_api_key = get_api_key("GROQ_API_KEY")
        self.openrouter_api_key = get_api_key("OPENROUTER_API_KEY")
        self.llm = None

        # 1. Try Groq Provider
        if self.groq_api_key:
            try:
                from langchain_groq import ChatGroq
                try:
                    self.llm = ChatGroq(model=groq_model, groq_api_key=self.groq_api_key, temperature=0.2)
                except Exception:
                    self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=self.groq_api_key, temperature=0.2)
            except Exception:
                self.llm = None

        # 2. Try OpenRouter Provider if Groq is unavailable
        if not self.llm and self.openrouter_api_key:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model=openrouter_model,
                    openai_api_key=self.openrouter_api_key,
                    openai_api_base="https://openrouter.ai/api/v1",
                    temperature=0.2
                )
            except Exception:
                self.llm = None

    def process(self, retrieval_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes final answer from retrieved chunks.
        
        Args:
            retrieval_payload: Output dict from RetrievalAgent.
            
        Returns:
            Dict: {answer, sources, category}
        """
        question = retrieval_payload.get("original_question", "")
        category = retrieval_payload.get("category", "off_topic")
        is_off_topic = retrieval_payload.get("is_off_topic", True)
        chunks = retrieval_payload.get("chunks", [])
        sources = retrieval_payload.get("sources", [])

        # Off-topic Redirect (no LLM call)
        if is_off_topic or category == "off_topic":
            return {
                "answer": self.OFF_TOPIC_RESPONSE,
                "sources": [],
                "category": "off_topic"
            }

        context_str = "\n\n".join([
            f"--- Document Source: {chunk['source']} ---\n{chunk['content']}"
            for chunk in chunks
        ])

        # Offline Fallback Synthesis across all retrieved chunks
        if not self.llm:
            formatted_chunks = []
            for idx, chunk in enumerate(chunks, 1):
                formatted_chunks.append(f"**From `{chunk['source']}`**:\n{chunk['content']}")

            fallback_text = (
                f"### Information retrieved for: \"{question}\"\n\n"
                + "\n\n---\n\n".join(formatted_chunks)
            )
            return {
                "answer": fallback_text,
                "sources": sources,
                "category": category
            }

        # LLM Synthesis Prompt
        prompt = f"""You are the Gemstone Knowledge Assistant, an expert gemological AI.
Answer the user question accurately and comprehensively based ONLY on the provided reference context documents.
Specifically list all relevant gemstone species, varieties, origins, features, or details requested.
Do not invent facts not contained in the context.

Context Information:
{context_str}

User Question: "{question}"

Answer:"""

        try:
            response = self.llm.invoke(prompt)
            return {
                "answer": response.content.strip(),
                "sources": sources,
                "category": category
            }
        except Exception:
            formatted_chunks = []
            for idx, chunk in enumerate(chunks, 1):
                formatted_chunks.append(f"**From `{chunk['source']}`**:\n{chunk['content']}")

            fallback_text = (
                f"### Information retrieved for: \"{question}\"\n\n"
                + "\n\n---\n\n".join(formatted_chunks)
            )
            return {
                "answer": fallback_text,
                "sources": sources,
                "category": category
            }
