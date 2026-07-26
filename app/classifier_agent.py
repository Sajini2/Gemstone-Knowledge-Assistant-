"""
Gemstone Knowledge Assistant - Agent 1: ClassifierAgent
Task: Domain Intent & Category Classification.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
from typing import Dict, Any
from app.config import get_api_key


class ClassifierAgent:
    """
    Agent 1: ClassifierAgent
    Classifies user questions into gemology categories or flags them as off-topic.
    """

    CATEGORIES = ["ruby", "sapphire", "moonstone", "sri_lankan_gems", "off_topic"]

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

    def process(self, question: str) -> Dict[str, Any]:
        """
        Classifies incoming raw question.
        
        Returns:
            Dict: {original_question, category, is_off_topic}
        """
        q_lower = question.lower()

        # Offline / Fallback Classification
        if not self.llm:
            if any(term in q_lower for term in ["france", "capital", "weather", "recipe", "math", "president", "code"]):
                if not any(gem in q_lower for gem in ["ruby", "sapphire", "moonstone", "gem", "jewel"]):
                    return {"original_question": question, "category": "off_topic", "is_off_topic": True}

            if "ruby" in q_lower or "pigeon" in q_lower or "spinel" in q_lower:
                cat = "ruby"
            elif "sapphire" in q_lower or "padparadscha" in q_lower:
                cat = "sapphire"
            elif "moonstone" in q_lower or "adularescence" in q_lower:
                cat = "moonstone"
            elif any(term in q_lower for term in ["sri lanka", "ceylon", "ratnapura", "ngja", "certification", "ethical", "mining"]):
                cat = "sri_lankan_gems"
            else:
                cat = "off_topic"

            return {"original_question": question, "category": cat, "is_off_topic": (cat == "off_topic")}

        # LLM Classification
        prompt = f"""Classify the user question into one of: ["ruby", "sapphire", "moonstone", "sri_lankan_gems", "off_topic"].
User Question: "{question}"

Return ONLY valid JSON:
{{
  "category": "<category>"
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
            category = parsed.get("category", "off_topic")
            
            return {
                "original_question": question,
                "category": category,
                "is_off_topic": (category == "off_topic")
            }
        except Exception:
            return {"original_question": question, "category": "off_topic", "is_off_topic": True}
