"""
Gemstone Knowledge Assistant - Agent Orchestrator
Coordinates message passing and workflow sequence between QueryAgent and GemstoneAgent.
"""

import json
from typing import Dict, Any

from app.query_agent import QueryAgent
from app.gemstone_agent import GemstoneAgent


def ask(question: str) -> Dict[str, Any]:
    """
    Orchestrates agent-to-agent communication for a user question.
    
    Workflow:
    1. Pass raw question to QueryAgent for intent classification and retrieval planning.
    2. Log QueryAgent output message to console.
    3. Pass QueryAgent payload to GemstoneAgent for retrieval execution and answer synthesis.
    4. Log GemstoneAgent output message to console.
    5. Return final response dictionary.
    
    Args:
        question: User query string.
        
    Returns:
        Dict containing answer, sources, and category.
    """
    print("=" * 70)
    print(f"[ORCHESTRATOR] Received User Question: \"{question}\"")
    print("=" * 70)

    # Step 1: Instantiate agents
    query_agent = QueryAgent()
    gemstone_agent = GemstoneAgent()

    # Step 2: QueryAgent processing
    print("[MESSAGE TRAIL: Step 1] Invoking QueryAgent...")
    query_payload = query_agent.process(question)
    
    print("[QUERY AGENT OUTPUT PAYLOAD]:")
    print(json.dumps(query_payload, indent=2))
    print("-" * 70)

    # Step 3: GemstoneAgent processing
    print("[MESSAGE TRAIL: Step 2] Invoking GemstoneAgent with QueryAgent Payload...")
    final_response = gemstone_agent.process(query_payload)

    print("[GEMSTONE AGENT FINAL RESPONSE]:")
    print(json.dumps(final_response, indent=2))
    print("=" * 70)

    return final_response
