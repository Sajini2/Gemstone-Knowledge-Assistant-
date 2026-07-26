"""
Gemstone Knowledge Assistant - 4-Agent Orchestrator
Coordinates sequential message passing across all 4 specialized AI agents:
1. ClassifierAgent (Intent & Category)
2. PlannerAgent (Query Optimization & Parameter Selection)
3. RetrievalAgent (Vector Store Search & Chunk Extraction)
4. SynthesizerAgent (Answer Generation & Fact Grounding)
"""

import json
from typing import Dict, Any

from app.classifier_agent import ClassifierAgent
from app.planner_agent import PlannerAgent
from app.retrieval_agent import RetrievalAgent
from app.synthesizer_agent import SynthesizerAgent


def ask(question: str) -> Dict[str, Any]:
    """
    Orchestrates 4-agent sequential workflow for a user question.
    
    Args:
        question: User query string.
        
    Returns:
        Dict containing answer, sources, and category.
    """
    print("=" * 70)
    print(f"[ORCHESTRATOR 4-AGENT SYSTEM] Received Question: \"{question}\"")
    print("=" * 70)

    # Step 1: Agent 1 - ClassifierAgent
    print("[MESSAGE TRAIL: Step 1] Invoking Agent 1 (ClassifierAgent)...")
    classifier_agent = ClassifierAgent()
    classification = classifier_agent.process(question)
    print("[AGENT 1 OUTPUT - CLASSIFICATION]:")
    print(json.dumps(classification, indent=2))
    print("-" * 70)

    # Step 2: Agent 2 - PlannerAgent
    print("[MESSAGE TRAIL: Step 2] Invoking Agent 2 (PlannerAgent)...")
    planner_agent = PlannerAgent()
    plan = planner_agent.process(classification)
    print("[AGENT 2 OUTPUT - RETRIEVAL PLAN]:")
    print(json.dumps(plan, indent=2))
    print("-" * 70)

    # Step 3: Agent 3 - RetrievalAgent
    print("[MESSAGE TRAIL: Step 3] Invoking Agent 3 (RetrievalAgent)...")
    retrieval_agent = RetrievalAgent()
    retrieval = retrieval_agent.process(plan)
    print("[AGENT 3 OUTPUT - RETRIEVED CONTEXT]:")
    print(f"  > Chunks Found: {len(retrieval.get('chunks', []))}")
    print(f"  > Sources: {retrieval.get('sources', [])}")
    print("-" * 70)

    # Step 4: Agent 4 - SynthesizerAgent
    print("[MESSAGE TRAIL: Step 4] Invoking Agent 4 (SynthesizerAgent)...")
    synthesizer_agent = SynthesizerAgent()
    final_response = synthesizer_agent.process(retrieval)
    print("[AGENT 4 OUTPUT - FINAL RESPONSE]:")
    print(json.dumps(final_response, indent=2))
    print("=" * 70)

    return final_response
