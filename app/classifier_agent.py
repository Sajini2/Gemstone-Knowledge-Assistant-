"""
Gemstone Knowledge Assistant - Agent 1: ClassifierAgent
Task: Domain Intent & Category Classification.
Supports Groq API and OpenRouter API providers.
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
    Supports Groq and OpenRouter LLMs.
    """

    CATEGORIES = ["ruby", "sapphire", "moonstone", "sri_lankan_gems", "off_topic"]

    def __init__(self, groq_model: str = "openai/gpt-oss-20b", openrouter_model: str = "openai/gpt-4o-mini"):
        self.groq_api_key = get_api_key("GROQ_API_KEY")
        self.openrouter_api_key = get_api_key("OPENROUTER_API_KEY")
        self.llm = None
        
        # 1. Try Groq Provider
        if self.groq_api_key:
            try:
                from langchain_groq import ChatGroq
                try:
                    self.llm = ChatGroq(model=groq_model, groq_api_key=self.groq_api_key, temperature=0.0)
                except Exception:
                    self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=self.groq_api_key, temperature=0.0)
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
                    temperature=0.0
                )
            except Exception:
                self.llm = None

    def process(self, question: str) -> Dict[str, Any]:
        """
        Classifies incoming raw question.
        
        Returns:
            Dict: {original_question, category, is_off_topic}
        """
        q_lower = question.lower()

        # Pre-check for clear gemstone domain keywords
        gemstone_keywords = [
            "gem", "gems", "gemstone", "gemstones", "jewel", "jewels", "mineral", "minerals",
            "ruby", "rubies", "sapphire", "sapphires", "moonstone", "moonstones", "sri lanka",
            "ceylon", "ratnapura", "ngja", "certif", "corundum", "feldspar", "spinel", "beryl"
        ]
        has_gem_keyword = any(kw in q_lower for kw in gemstone_keywords)

        # Offline / Fallback Classification
        if not self.llm:
            if not has_gem_keyword and any(term in q_lower for term in ["france", "capital", "weather", "recipe", "math", "president", "code", "python"]):
                return {"original_question": question, "category": "off_topic", "is_off_topic": True}

            if "ruby" in q_lower or "rubies" in q_lower or "pigeon" in q_lower:
                cat = "ruby"
            elif "sapphire" in q_lower or "sapphires" in q_lower or "padparadscha" in q_lower:
                cat = "sapphire"
            elif "moonstone" in q_lower or "moonstones" in q_lower or "adularescence" in q_lower:
                cat = "moonstone"
            elif has_gem_keyword or any(term in q_lower for term in ["sri lanka", "ceylon", "ratnapura", "ngja", "certif", "ethical", "mining"]):
                cat = "sri_lankan_gems"
            else:
                cat = "off_topic"

            return {"original_question": question, "category": cat, "is_off_topic": (cat == "off_topic")}

        # LLM Classification Prompt with Clear Domain Guidance
        prompt = f"""Classify the user question into EXACTLY ONE of these categories:
- "ruby": questions about ruby corundum, origins, inclusions, or valuation.
- "sapphire": questions about sapphire varieties, padparadscha, or star sapphires.
- "moonstone": questions about moonstone, adularescence, or feldspar.
- "sri_lankan_gems": questions about Sri Lankan gems, gem types/species, Ratnapura mining, Ceylon gem trade, or gem certification.
- "off_topic": ONLY questions completely unrelated to gemstones or gemology (e.g. capital cities, sports, weather, cooking, programming).

CRITICAL RULE: Any question asking about gems, gemstones, gem types, species, mining, minerals, or Sri Lankan gemology is ON-TOPIC (classify as "sri_lankan_gems" if not ruby/sapphire/moonstone specific).

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
            category = parsed.get("category", "off_topic").lower()

            # Override if question has gemstone keywords but LLM misclassified
            if category == "off_topic" and has_gem_keyword:
                category = "sri_lankan_gems"
            
            return {
                "original_question": question,
                "category": category,
                "is_off_topic": (category == "off_topic")
            }
        except Exception:
            cat = "sri_lankan_gems" if has_gem_keyword else "off_topic"
            return {"original_question": question, "category": cat, "is_off_topic": (cat == "off_topic")}
