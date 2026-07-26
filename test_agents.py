"""
Gemstone Knowledge Assistant - Multi-Agent System Test Script
Executes full message trail testing across 5 domain benchmark queries and 1 off-topic test.
"""

import sys
import os

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.orchestrator import ask

TEST_QUESTIONS = [
    "What is Ruby?",
    "What is Sapphire?",
    "What is Moonstone?",
    "What is Gem Certification?",
    "Which gems are found in Sri Lanka?",
    "What's the capital of France?"  # Off-topic redirect test
]


def run_agent_tests():
    print("=" * 80)
    print("  GEMSTONE KNOWLEDGE ASSISTANT - MULTI-AGENT ORCHESTRATION SUITE")
    print("=" * 80)

    results = []
    for idx, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n>>> TEST CASE {idx}/{len(TEST_QUESTIONS)} <<<")
        response = ask(question)
        answer_text = response.get("answer", "")
        # Safe ASCII encoding preview for Windows console compatibility
        safe_preview = answer_text[:120].encode('ascii', errors='replace').decode('ascii') + "..."
        
        results.append({
            "test_case": idx,
            "question": question,
            "category": response.get("category"),
            "sources": response.get("sources", []),
            "answer_preview": safe_preview
        })

    print("\n" + "=" * 80)
    print("  AGENT TEST SUMMARY RESULTS")
    print("=" * 80)
    for res in results:
        status = "[OFF-TOPIC REDIRECT]" if res["category"] == "off_topic" else "[GROUNDED ANSWER]"
        print(f"Test {res['test_case']} ({res['category']}): {res['question']} -> {status}")
        print(f"   Sources: {res['sources']}")
        print(f"   Answer Snippet: {res['answer_preview']}\n")
    print("=" * 80)


if __name__ == "__main__":
    run_agent_tests()
