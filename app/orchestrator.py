"""
Gemstone Knowledge Assistant - 4-Agent Orchestrator
Coordinates sequential message passing across all 4 specialized AI agents:
1. ClassifierAgent (Intent & Category)
2. PlannerAgent (Query Optimization & Parameter Selection)
3. RetrievalAgent (Vector Store Search & Chunk Extraction)
4. SynthesizerAgent (Answer Generation & Fact Grounding)
"""

import sys
import json
from typing import Dict, Any

from app.classifier_agent import ClassifierAgent
from app.planner_agent import PlannerAgent
from app.retrieval_agent import RetrievalAgent
from app.synthesizer_agent import SynthesizerAgent


def _safe_print(obj: Any):
    """Prints objects safely without throwing UnicodeEncodeError on Windows CP1252 consoles."""
    if isinstance(obj, (dict, list)):
        try:
            print(json.dumps(obj, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(obj, indent=2, ensure_ascii=True))
    else:
        try:
            print(obj)
        except UnicodeEncodeError:
            encoding = sys.stdout.encoding or "utf-8"
            print(str(obj).encode(encoding, errors="replace").decode(encoding, errors="replace"))


def ask(question: str) -> Dict[str, Any]:
    """
    Orchestrates 4-agent sequential workflow for a user question.
    
    Args:
        question: User query string.
        
    Returns:
        Dict containing answer, sources, and category.
    """
    _safe_print("=" * 70)
    _safe_print(f'[ORCHESTRATOR 4-AGENT SYSTEM] Received Question: "{question}"')
    _safe_print("=" * 70)

    # Step 1: Agent 1 - ClassifierAgent
    _safe_print("[MESSAGE TRAIL: Step 1] Invoking Agent 1 (ClassifierAgent)...")
    classifier_agent = ClassifierAgent()
    classification = classifier_agent.process(question)
    _safe_print("[AGENT 1 OUTPUT - CLASSIFICATION]:")
    _safe_print(classification)
    _safe_print("-" * 70)

    # Step 2: Agent 2 - PlannerAgent
    _safe_print("[MESSAGE TRAIL: Step 2] Invoking Agent 2 (PlannerAgent)...")
    planner_agent = PlannerAgent()
    plan = planner_agent.process(classification)
    _safe_print("[AGENT 2 OUTPUT - RETRIEVAL PLAN]:")
    _safe_print(plan)
    _safe_print("-" * 70)

    # Step 3: Agent 3 - RetrievalAgent
    _safe_print("[MESSAGE TRAIL: Step 3] Invoking Agent 3 (RetrievalAgent)...")
    retrieval_agent = RetrievalAgent()
    retrieval = retrieval_agent.process(plan)
    _safe_print("[AGENT 3 OUTPUT - RETRIEVED CONTEXT]:")
    _safe_print(f"  > Chunks Found: {len(retrieval.get('chunks', []))}")
    _safe_print(f"  > Sources: {retrieval.get('sources', [])}")
    _safe_print("-" * 70)

    # Step 4: Agent 4 - SynthesizerAgent
    _safe_print("[MESSAGE TRAIL: Step 4] Invoking Agent 4 (SynthesizerAgent)...")
    synthesizer_agent = SynthesizerAgent()
    final_response = synthesizer_agent.process(retrieval)
    _safe_print("[AGENT 4 OUTPUT - FINAL RESPONSE]:")
    _safe_print(final_response)
    _safe_print("=" * 70)

    return final_response
