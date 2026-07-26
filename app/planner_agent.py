"""
Gemstone Knowledge Assistant - Agent 2: PlannerAgent
Task: Retrieval Planning, Query Optimization, and Parameter Selection.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
from typing import Dict, Any
from app.config import get_api_key


class PlannerAgent:
    """
    Agent 2: PlannerAgent
    Accepts classification from ClassifierAgent and plans optimal vector search parameters.
    """

    def __init__(self, model_name: str = "openai/gpt-oss-20b"):
        self.model_name = model_name
        self.api_key = get_api_key("GROQ_API_KEY")
        self.llm = None
        
        if self.api_key:
            try:
                from langchain_groq import ChatGroq
                try:
                    self.llm = ChatGroq(model=self.model_name, groq_api_key=self.api_key, temperature=0.0)
                except Exception:
                    self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=self.api_key, temperature=0.0)
            except Exception:
                self.llm = None

    def process(self, classification_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plans retrieval parameters based on classification output.
        
        Args:
            classification_payload: Output dict from ClassifierAgent.
            
        Returns:
            Dict: {original_question, category, is_off_topic, retrieval_query, k}
        """
        question = classification_payload.get("original_question", "")
        category = classification_payload.get("category", "off_topic")
        is_off_topic = classification_payload.get("is_off_topic", True)

        if is_off_topic or category == "off_topic":
            return {
                "original_question": question,
                "category": "off_topic",
                "is_off_topic": True,
                "retrieval_query": "",
                "k": 0
            }

        # Offline / Fallback Retrieval Query Rewriting
        if not self.llm:
            domain_keywords = {
                "ruby": "ruby corundum inclusions geological origin heat treatment valuation",
                "sapphire": "sapphire color varieties padparadscha star sapphires valuation",
                "moonstone": "moonstone adularescence feldspar meetiyagoda formation jewelry",
                "sri_lankan_gems": "sri lanka ratnapura ngja gem certification species ethical mining"
            }
            prefix = domain_keywords.get(category, "gemstone")
            return {
                "original_question": question,
                "category": category,
                "is_off_topic": False,
                "retrieval_query": f"{prefix} {question}",
                "k": 4
            }

        # LLM Retrieval Planning
        prompt = f"""You are a RAG retrieval planner. Optimize the search query for semantic vector lookup.
Category: "{category}"
User Question: "{question}"

Return ONLY valid JSON:
{{
  "retrieval_query": "<rephrased_optimized_query>",
  "k": 4
}}"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            parsed = json.loads(content.strip())
            retrieval_query = parsed.get("retrieval_query", question)
            k = parsed.get("k", 4)
            
            return {
                "original_question": question,
                "category": category,
                "is_off_topic": False,
                "retrieval_query": retrieval_query,
                "k": k
            }
        except Exception:
            return {
                "original_question": question,
                "category": category,
                "is_off_topic": False,
                "retrieval_query": question,
                "k": 4
            }
