"""
Gemstone Knowledge Assistant - Streamlit Web Application
Interactive web interface for multi-agent gemstone domain Q&A and RAG retrieval.
"""

import sys
import os
import streamlit as st

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.orchestrator import ask

# Page Configuration
st.set_page_config(
    page_title="Gemstone Knowledge Assistant",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling (Vanilla CSS)
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .category-badge {
        display: inline-block;
        background-color: #DBEAFE;
        color: #1E40AF;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        margin-bottom: 1rem;
    }
    .source-tag {
        display: inline-block;
        background-color: #F1F5F9;
        color: #475569;
        font-size: 0.85rem;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        border: 1px solid #CBD5E1;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header Section
    st.markdown('<div class="main-title">💎 Gemstone Knowledge Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">An Agentic AI RAG system specializing in Rubies, Sapphires, Moonstones, and Sri Lankan Gemology.</div>',
        unsafe_allow_html=True
    )

    # Sidebar Information
    with st.sidebar:
        st.header("About")
        st.info(
            "This application uses a specialized **4-Agent RAG System**:\n\n"
            "- **ClassifierAgent**: Intent & domain classification.\n"
            "- **PlannerAgent**: Query optimization & search strategy.\n"
            "- **RetrievalAgent**: ChromaDB vector search & context extraction.\n"
            "- **SynthesizerAgent**: Answer synthesis, source citation, & off-topic guard.\n\n"
            "**Knowledge Base**: 20 factual reference documents."
        )
        st.markdown("---")
        st.subheader("Sample Queries")
        st.caption("• What is Ruby?")
        st.caption("• What is Sapphire?")
        st.caption("• What is Moonstone?")
        st.caption("• What is Gem Certification?")
        st.caption("• Which gems are found in Sri Lanka?")

    # User Question Input Form
    with st.form(key="query_form"):
        user_question = st.text_input(
            "Ask any question about gemstones:",
            placeholder="e.g., What are the key valuation factors of ruby?",
            key="question_input"
        )
        submit_button = st.form_submit_button(label="Ask Assistant 💎", use_container_width=True)

    # Response Display
    if submit_button and user_question.strip():
        with st.spinner("Analyzing question and retrieving gemstone knowledge..."):
            try:
                # Invoke Orchestrator
                response = ask(user_question.strip())

                category = response.get("category", "general")
                answer = response.get("answer", "No answer generated.")
                sources = response.get("sources", [])

                # Render Answer Box
                st.markdown("---")
                st.subheader("Answer")
                
                # Render Category Badge
                st.markdown(f'<span class="category-badge">Category: {category.upper()}</span>', unsafe_allow_html=True)
                
                st.markdown(answer)

                # Render Grounded Sources Section
                st.markdown("---")
                st.subheader("Grounded Sources")
                if sources:
                    st.write("Information retrieved from the following reference documents:")
                    for src in sources:
                        st.markdown(f"- 📄 `{src}`")
                else:
                    st.caption("No reference documents required for this query (e.g., off-topic response).")

            except Exception as e:
                st.error("Something went wrong — please try again in a moment.")


if __name__ == "__main__":
    main()
