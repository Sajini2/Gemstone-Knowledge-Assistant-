"""
Gemstone Knowledge Assistant - Agent 4: SynthesizerAgent
Task: RAG Response Synthesis, Factual Grounding, and Off-Topic Filtering.
"""

from typing import Dict, Any, List
from app.config import get_api_key


class SynthesizerAgent:
    """
    Agent 4: SynthesizerAgent
    Consumes retrieved context chunks from RetrievalAgent and synthesizes source-grounded answers.
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
                try:
                    self.llm = ChatGroq(model=self.model_name, groq_api_key=self.api_key, temperature=0.2)
                except Exception:
                    self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=self.api_key, temperature=0.2)
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

        # Offline Fallback Synthesis
        if not self.llm:
            fallback_text = (
                f"Based on reference documents ({', '.join(sources)}): "
                f"Here is the retrieved context answering '{question}':\n"
                f"{chunks[0]['content'] if chunks else 'No relevant context found.'}"
            )
            return {
                "answer": fallback_text,
                "sources": sources,
                "category": category
            }

        # LLM Synthesis
        prompt = f"""You are the Gemstone Knowledge Assistant, an expert gemological AI.
Answer the user question accurately based ONLY on the provided reference context documents.
Do not invent facts. Cite key details directly from the context.

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
            fallback_text = (
                f"Retrieved Context ({', '.join(sources)}):\n"
                f"{chunks[0]['content'] if chunks else 'No context retrieved.'}"
            )
            return {
                "answer": fallback_text,
                "sources": sources,
                "category": category
            }
