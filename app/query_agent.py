"""
Gemstone Knowledge Assistant - Query Agent
Classifies user questions, performs retrieval planning, and formulates optimized search queries.
"""

import os
import json
from typing import Dict, Any

from app.config import get_api_key


class QueryAgent:
    """
    QueryAgent classifies incoming gemstone questions into specific domain categories
    and plans optimal retrieval parameters (rephrased query and top-k count).
    """

    CATEGORIES = ["ruby", "sapphire", "moonstone", "sri_lankan_gems", "off_topic"]

    def __init__(self, model_name: str = "openai/gpt-oss-20b"):
        self.model_name = model_name
        self.api_key = get_api_key("GROQ_API_KEY")
        self.llm = None
        
        if self.api_key:
            try:
                from langchain_groq import ChatGroq
                # Attempt initialization with requested model, fallback to llama-3.3-70b-versatile if model not accessible
                try:
                    self.llm = ChatGroq(model=self.model_name, groq_api_key=self.api_key, temperature=0.0)
                except Exception:
                    self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=self.api_key, temperature=0.0)
            except Exception:
                self.llm = None

    def _rule_based_classify(self, question: str) -> Dict[str, Any]:
        """Fallback rule-based classifier and query planner when LLM API is offline or key missing."""
        q_lower = question.lower()

        # Off-topic checks
        if any(term in q_lower for term in ["france", "capital", "weather", "recipe", "math", "president", "football", "code"]):
            if not any(gem in q_lower for gem in ["ruby", "sapphire", "moonstone", "gem", "jewel"]):
                return {
                    "original_question": question,
                    "category": "off_topic",
                    "retrieval_query": "",
                    "k": 0,
                    "needs_retrieval": False
                }

        # Category classification
        if "ruby" in q_lower or "pigeon" in q_lower or "spinel" in q_lower:
            category = "ruby"
            retrieval_query = f"ruby gemstone properties inclusions origin valuation {question}"
        elif "padparadscha" in q_lower or "sapphire" in q_lower or "star sapphire" in q_lower:
            category = "sapphire"
            retrieval_query = f"sapphire corundum color varieties valuation {question}"
        elif "moonstone" in q_lower or "adularescence" in q_lower or "schiller" in q_lower:
            category = "moonstone"
            retrieval_query = f"moonstone adularescence feldspar properties sources {question}"
        elif any(term in q_lower for term in ["sri lanka", "ceylon", "ratnapura", "ngja", "certification", "ethical", "mining"]):
            category = "sri_lankan_gems"
            retrieval_query = f"sri lanka gemstone mining ngja certification species {question}"
        else:
            category = "off_topic"
            return {
                "original_question": question,
                "category": "off_topic",
                "retrieval_query": "",
                "k": 0,
                "needs_retrieval": False
            }

        return {
            "original_question": question,
            "category": category,
            "retrieval_query": retrieval_query,
            "k": 4,
            "needs_retrieval": True
        }

    def process(self, question: str) -> Dict[str, Any]:
        """
        Processes a raw user question, classifies intent, and determines retrieval plan.
        
        Args:
            question: Raw user question string.
            
        Returns:
            Dict containing original_question, category, retrieval_query, k, and needs_retrieval.
        """
        if not self.llm:
            return self._rule_based_classify(question)

        prompt = f"""You are an expert AI classifier and retrieval planner for a Gemstone Knowledge Assistant.
Analyze the user question and return a valid JSON object with the following fields:
- "category": Must be one of ["ruby", "sapphire", "moonstone", "sri_lankan_gems", "off_topic"].
- "needs_retrieval": boolean (false if "off_topic", true otherwise).
- "retrieval_query": string (an optimized search query for vector retrieval, or empty string if off_topic).
- "k": integer (number of chunks to retrieve, e.g., 4, or 0 if off_topic).

User Question: "{question}"

Return ONLY JSON format:
{{
  "category": "<category>",
  "needs_retrieval": <true_or_false>,
  "retrieval_query": "<optimized_query>",
  "k": <number>
}}"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            # Clean markdown JSON block formatting if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            parsed = json.loads(content)
            category = parsed.get("category", "off_topic")
            needs_retrieval = parsed.get("needs_retrieval", category != "off_topic")
            
            if category == "off_topic" or not needs_retrieval:
                return {
                    "original_question": question,
                    "category": "off_topic",
                    "retrieval_query": "",
                    "k": 0,
                    "needs_retrieval": False
                }

            return {
                "original_question": question,
                "category": category,
                "retrieval_query": parsed.get("retrieval_query", question),
                "k": parsed.get("k", 4),
                "needs_retrieval": True
            }

        except Exception:
            return self._rule_based_classify(question)
