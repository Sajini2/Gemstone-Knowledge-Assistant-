"""
Gemstone Knowledge Assistant - Modern Interactive Streamlit Web Application
Luxury dark glassmorphism interface powered by a specialized 4-Agent RAG pipeline.
"""

import sys
import os
import streamlit as st

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.orchestrator import ask

# Page Configuration - Hide sidebar completely for clean single-page app
st.set_page_config(
    page_title="Gemstone Knowledge Assistant",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Glassmorphism & Vibrant Dark Theme CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

    /* Global Theme Overrides */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1E1B4B 0%, #0F172A 45%, #020617 100%);
        color: #F8FAFC;
    }

    /* Hide Sidebar Completely */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Hero Header Styling */
    .hero-container {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 40%, #C084FC 80%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        max-width: 650px;
        margin: 0 auto 1.8rem auto;
        line-height: 1.6;
    }

    /* Quick Prompt Chips */
    .chip-container-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        margin-bottom: 0.6rem;
        text-align: center;
    }

    /* Glassmorphism Card Container */
    .glass-card {
        background: rgba(30, 41, 59, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }

    /* Dynamic Category Badges */
    .badge-ruby {
        background: linear-gradient(135deg, #EF4444 0%, #991B1B 100%);
        color: #FFFFFF;
    }
    .badge-sapphire {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: #FFFFFF;
    }
    .badge-moonstone {
        background: linear-gradient(135deg, #A855F7 0%, #6B21A8 100%);
        color: #FFFFFF;
    }
    .badge-sri_lankan_gems {
        background: linear-gradient(135deg, #10B981 0%, #065F46 100%);
        color: #FFFFFF;
    }
    .badge-off_topic {
        background: linear-gradient(135deg, #F59E0B 0%, #78350F 100%);
        color: #FFFFFF;
    }
    .badge-general {
        background: linear-gradient(135deg, #64748B 0%, #334155 100%);
        color: #FFFFFF;
    }
    .category-badge-pill {
        display: inline-block;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.82rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        margin-bottom: 1rem;
    }

    /* Grounded Source Tags */
    .source-tag-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38BDF8;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        margin: 0.25rem 0.3rem 0.25rem 0;
        transition: all 0.2s ease;
    }
    .source-tag-pill:hover {
        border-color: #818CF8;
        color: #818CF8;
    }

    /* Agent Info Pills */
    .agent-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        color: #CBD5E1;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize query session state."""
    if "user_query" not in st.session_state:
        st.session_state.user_query = ""


def set_query(prompt_text: str):
    """Callback for sample query chip selection."""
    st.session_state.user_query = prompt_text


def main():
    init_session_state()

    # Hero Header Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">💎 Gemstone Knowledge Assistant</div>
        <div class="hero-subtitle">
            An intelligent Multi-Agent RAG system specializing in Rubies, Sapphires, Moonstones, 
            and Sri Lankan Gemology.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Sample Query Chips
    st.markdown('<div class="chip-container-label">✨ Quick Topics to Explore</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("💎 Rubies", use_container_width=True):
            set_query("What are the key valuation factors of ruby?")
    with col2:
        if st.button("💙 Sapphires", use_container_width=True):
            set_query("What is Padparadscha Sapphire?")
    with col3:
        if st.button("🌙 Moonstone", use_container_width=True):
            set_query("How does adularescence work in moonstone?")
    with col4:
        if st.button("🇱🇰 Sri Lanka Gems", use_container_width=True):
            set_query("What are the Sri Lankan gems?")
    with col5:
        if st.button("📜 Certification", use_container_width=True):
            set_query("How does NGJA gem certification work?")

    st.markdown("<br>", unsafe_allow_html=True)

    # Question Input Form
    with st.form(key="query_form", clear_on_submit=False):
        user_question = st.text_input(
            "Ask any question about gemstones:",
            value=st.session_state.user_query,
            placeholder="e.g., Which rare gem species are found in Sri Lanka?",
            key="input_box"
        )
        submit_button = st.form_submit_button(label="Ask Assistant 💎", use_container_width=True)

    # Execution & Response Card
    if submit_button and user_question.strip():
        # Update session state to match typed question
        st.session_state.user_query = user_question.strip()
        
        with st.spinner("⚡ 4-Agent Pipeline active (Classifier → Planner → Retrieval → Synthesizer)..."):
            try:
                # Call Orchestrator
                response = ask(user_question.strip())

                category = response.get("category", "general").lower()
                answer = response.get("answer", "No answer generated.")
                sources = response.get("sources", [])

                # Map badge CSS class
                badge_class = f"badge-{category}" if f"badge-{category}" in [
                    "badge-ruby", "badge-sapphire", "badge-moonstone", "badge-sri_lankan_gems", "badge-off_topic"
                ] else "badge-general"

                # Render Main Answer Card
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="glass-card">
                    <span class="category-badge-pill {badge_class}">Domain: {category.replace('_', ' ').upper()}</span>
                    <div style="font-size: 1.05rem; line-height: 1.7; color: #F1F5F9;">
                        {answer}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Render Grounded Sources Section
                if sources:
                    st.markdown("### 📄 Grounded Reference Sources")
                    st.caption("Information retrieved directly from the following knowledge base files:")
                    
                    sources_html = "".join([
                        f'<span class="source-tag-pill">📄 {src}</span>'
                        for src in sources
                    ])
                    st.markdown(f'<div style="margin-bottom: 1.5rem;">{sources_html}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error("Something went wrong with the multi-agent pipeline. Please try again in a moment.")

    st.markdown("---")

    # 4-Agent Architecture Accordion Footer
    with st.expander("🛠️ View 4-Agent Architecture Pipeline Details"):
        st.markdown("""
        The **Gemstone Knowledge Assistant** runs on a 4-agent sequential workflow:
        
        - 🤖 **Agent 1: ClassifierAgent** — Identifies user intent and classifies category (`ruby`, `sapphire`, `moonstone`, `sri_lankan_gems`, `off_topic`).
        - 🧠 **Agent 2: PlannerAgent** — Optimizes semantic vector search queries and plans retrieval parameters ($k=4$).
        - 🔍 **Agent 3: RetrievalAgent** — Performs vector search against persistent **ChromaDB** using `all-MiniLM-L6-v2` ONNX embeddings.
        - ✨ **Agent 4: SynthesizerAgent** — Grounded LLM synthesis (`openai/gpt-oss-120b`) producing cited answers or polite off-topic redirects.
        """)


if __name__ == "__main__":
    main()
