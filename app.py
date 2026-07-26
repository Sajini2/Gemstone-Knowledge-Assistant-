"""
Gemstone Knowledge Assistant - Streamlit Web Application (Root Entrypoint)
Luxury dark glassmorphism interface optimized for Desktop, Tablet, and Mobile devices.
"""

import sys
import os
import streamlit as st

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.orchestrator import ask

# Page Configuration - Single page responsive layout
st.set_page_config(
    page_title="Gemstone Knowledge Assistant",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Mobile-First Responsive Glassmorphism & Dark Theme CSS)
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

    /* Main Container Padding Adjustment */
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 800px;
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
        padding: 1rem 0 0.8rem 0;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 40%, #C084FC 80%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        max-width: 650px;
        margin: 0 auto 1.4rem auto;
        line-height: 1.5;
    }

    /* Quick Prompt Chips Label */
    .chip-container-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    /* Glassmorphism Card Container */
    .glass-card {
        background: rgba(30, 41, 59, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
    }

    /* Dynamic Category Badges */
    .badge-ruby { background: linear-gradient(135deg, #EF4444 0%, #991B1B 100%); color: #FFFFFF; }
    .badge-sapphire { background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%); color: #FFFFFF; }
    .badge-moonstone { background: linear-gradient(135deg, #A855F7 0%, #6B21A8 100%); color: #FFFFFF; }
    .badge-sri_lankan_gems { background: linear-gradient(135deg, #10B981 0%, #065F46 100%); color: #FFFFFF; }
    .badge-off_topic { background: linear-gradient(135deg, #F59E0B 0%, #78350F 100%); color: #FFFFFF; }
    .badge-general { background: linear-gradient(135deg, #64748B 0%, #334155 100%); color: #FFFFFF; }

    .category-badge-pill {
        display: inline-block;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        margin-bottom: 0.9rem;
    }

    /* Grounded Source Tags */
    .source-tag-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38BDF8;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.28rem 0.75rem;
        border-radius: 8px;
        margin: 0.2rem 0.25rem 0.2rem 0;
        word-break: break-all;
    }

    /* Form Inputs Ergonomics */
    .stTextInput input {
        border-radius: 10px !important;
        padding: 0.6rem 0.9rem !important;
        font-size: 0.95rem !important;
    }
    .stButton button {
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* MOBILE RESPONSIVE MEDIA QUERIES (under 768px) */
    @media screen and (max-width: 768px) {
        .main .block-container {
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }
        .hero-title {
            font-size: 1.85rem !important;
            margin-bottom: 0.3rem !important;
        }
        .hero-subtitle {
            font-size: 0.9rem !important;
            margin-bottom: 1rem !important;
        }
        .glass-card {
            padding: 1rem !important;
            border-radius: 12px !important;
        }
        .category-badge-pill {
            font-size: 0.72rem !important;
            padding: 0.25rem 0.65rem !important;
        }
        .source-tag-pill {
            font-size: 0.75rem !important;
            padding: 0.22rem 0.55rem !important;
        }
        /* Touch friendly buttons on mobile */
        .stButton button {
            padding: 0.5rem 0.5rem !important;
            font-size: 0.82rem !important;
        }
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

    # Responsive Quick Topics Section
    st.markdown('<div class="chip-container-label">✨ Quick Topics to Explore</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
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
        if st.button("🇱🇰 LK Gems", use_container_width=True):
            set_query("What are the Sri Lankan gems?")
    with col5:
        if st.button("📜 Certify", use_container_width=True):
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
                    <div style="font-size: 1rem; line-height: 1.65; color: #F1F5F9;">
                        {answer}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Render Grounded Sources Section
                if sources:
                    st.markdown("### 📄 Grounded Reference Sources")
                    st.caption("Information retrieved directly from reference knowledge files:")
                    
                    sources_html = "".join([
                        f'<span class="source-tag-pill">📄 {src}</span>'
                        for src in sources
                    ])
                    st.markdown(f'<div style="margin-bottom: 1.5rem; line-height: 1.8;">{sources_html}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error("Something went wrong with the multi-agent pipeline. Please try again in a moment.")

    st.markdown("---")

    # 4-Agent Architecture Accordion Footer
    with st.expander("🛠️ View 4-Agent Architecture Pipeline Details"):
        st.markdown("""
        The **Gemstone Knowledge Assistant** runs on a specialized 4-agent sequential workflow:
        
        - 🤖 **Agent 1: ClassifierAgent** — Identifies user intent and classifies category (`ruby`, `sapphire`, `moonstone`, `sri_lankan_gems`, `off_topic`).
        - 🧠 **Agent 2: PlannerAgent** — Optimizes semantic vector search queries and plans retrieval parameters ($k=4$).
        - 🔍 **Agent 3: RetrievalAgent** — Performs vector search against persistent **ChromaDB** using `all-MiniLM-L6-v2` ONNX embeddings.
        - ✨ **Agent 4: SynthesizerAgent** — Grounded LLM synthesis (`openai/gpt-oss-120b`) producing cited answers or polite off-topic redirects.
        """)


if __name__ == "__main__":
    main()
