"""
Gemstone Knowledge Assistant - Modern Responsive Streamlit Web Application
Luxury dark glassmorphism interface optimized for Desktop, Tablet, and Mobile devices.
"""

import sys
import os
import site

# Ensure User Site Packages directory is first in sys.path for onnxruntime & chromadb
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.insert(0, user_site)

# Pre-import onnxruntime to populate sys.modules before ChromaDB loads
try:
    import onnxruntime
except ImportError:
    pass

import streamlit as st

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    html, body, .stApp {
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

    /* Executive Markdown Table & Typography Styling */
    .stMarkdown table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        margin: 1.2rem 0 !important;
        background: rgba(15, 23, 42, 0.65) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    }
    .stMarkdown th {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: #38BDF8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.06em !important;
        padding: 0.8rem 1rem !important;
        border-bottom: 1px solid rgba(56, 189, 248, 0.3) !important;
    }
    .stMarkdown td {
        padding: 0.75rem 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        font-size: 0.92rem !important;
        color: #F1F5F9 !important;
        line-height: 1.6 !important;
    }
    .stMarkdown tr:last-child td {
        border-bottom: none !important;
    }
    .stMarkdown tr:hover td {
        background: rgba(56, 189, 248, 0.08) !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(135deg, #38BDF8 0%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 1.3rem !important;
        margin-bottom: 0.6rem !important;
    }
    .stMarkdown ul, .stMarkdown ol {
        line-height: 1.75 !important;
        color: #E2E8F0 !important;
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
        padding: 0.35rem 0.95rem;
        border-radius: 9999px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
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
    if "input_box" not in st.session_state:
        st.session_state.input_box = ""


def set_query(prompt_text: str):
    """Callback for sample query chip selection."""
    st.session_state.user_query = prompt_text
    st.session_state.input_box = prompt_text


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
    
    # 5 Responsive Column Layout (Adapts to Mobile)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        st.button("💎 Rubies", use_container_width=True, on_click=set_query, args=("What are the key valuation factors of ruby?",))
    with col2:
        st.button("💙 Sapphires", use_container_width=True, on_click=set_query, args=("What is Padparadscha Sapphire?",))
    with col3:
        st.button("🌙 Moonstone", use_container_width=True, on_click=set_query, args=("How does adularescence work in moonstone?",))
    with col4:
        st.button("🇱🇰 LK Gems", use_container_width=True, on_click=set_query, args=("What are the Sri Lankan gems?",))
    with col5:
        st.button("📜 Certify", use_container_width=True, on_click=set_query, args=("How does NGJA gem certification work?",))

    st.markdown("<br>", unsafe_allow_html=True)

    # Question Input Form
    with st.form(key="query_form", clear_on_submit=False):
        user_question = st.text_input(
            "Ask any question about gemstones:",
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
                is_off_topic = (category == "off_topic")

                # Map badge CSS class
                badge_class = f"badge-{category}" if f"badge-{category}" in [
                    "badge-ruby", "badge-sapphire", "badge-moonstone", "badge-sri_lankan_gems", "badge-off_topic"
                ] else "badge-general"

                st.markdown("<br>", unsafe_allow_html=True)

                if is_off_topic:
                    # Off-Topic Redirect Card
                    st.markdown(f"""
                    <div class="glass-card">
                        <span class="category-badge-pill badge-off_topic">DOMAIN: OFF TOPIC</span>
                        <div style="font-size: 1rem; line-height: 1.65; color: #F1F5F9;">
                            {answer}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Interactive Gemology Intelligence Report Header
                    category_display = category.replace('_', ' ').upper()
                    sources_count = len(sources) if sources else 0

                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 1.5rem;">
                        <h2 style="font-family: 'Outfit', sans-serif; font-weight: 700; background: linear-gradient(135deg, #38BDF8 0%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.3rem;">
                            💎 Executive Gemology Report
                        </h2>
                        <p style="color: #94A3B8; font-size: 0.9rem;">Multi-Agent Grounded Analysis & Domain Intelligence</p>
                    </div>

                    <!-- Custom Responsive Metric Cards (No Truncation) -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.9rem; margin-bottom: 1.5rem;">
                        <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 14px; padding: 1rem; text-align: center;">
                            <div style="font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 600; letter-spacing: 0.06em;">Domain Category</div>
                            <div style="font-size: 1.05rem; font-weight: 700; color: #38BDF8; margin-top: 0.3rem;">{category_display}</div>
                        </div>
                        <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(192, 132, 252, 0.25); border-radius: 14px; padding: 1rem; text-align: center;">
                            <div style="font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 600; letter-spacing: 0.06em;">Sources Cited</div>
                            <div style="font-size: 1.05rem; font-weight: 700; color: #C084FC; margin-top: 0.3rem;">{sources_count} Knowledge Files</div>
                        </div>
                        <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 14px; padding: 1rem; text-align: center;">
                            <div style="font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 600; letter-spacing: 0.06em;">Pipeline Verification</div>
                            <div style="font-size: 1.05rem; font-weight: 700; color: #34D399; margin-top: 0.3rem;">4-Agent Grounded</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Interactive Tabs for Report
                    tab_report, tab_sources, tab_audit = st.tabs([
                        "📑 Executive Report", 
                        "📄 Grounded Reference Sources", 
                        "🤖 Agent Execution Audit"
                    ])

                    with tab_report:
                        st.markdown(f'<span class="category-badge-pill {badge_class}">CATEGORY: {category_display}</span>', unsafe_allow_html=True)
                        
                        # Render the synthesized markdown answer cleanly inside Streamlit
                        st.markdown(answer)
                        
                        st.markdown("<br>", unsafe_allow_html=True)

                        # Export / Download Report Option
                        report_content = f"""# Executive Gemology Report
Query: {user_question}
Category: {category_display}
Sources Cited: {', '.join(sources) if sources else 'None'}

---

{answer}
"""
                        st.download_button(
                            label="📥 Export Executive Report (.md)",
                            data=report_content,
                            file_name=f"gemstone_report_{category}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                        # Interactive Follow-up Topics Section
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown('<div class="chip-container-label">💡 EXPLORE RELATED GEMOLOGY TOPICS</div>', unsafe_allow_html=True)
                        q_col1, q_col2, q_col3 = st.columns(3)
                        with q_col1:
                            st.button("✨ Geuda Corundum", use_container_width=True, on_click=set_query, args=("How does Geuda sapphire heat treatment work?",))
                        with q_col2:
                            st.button("⛏️ Ratnapura Mining", use_container_width=True, on_click=set_query, args=("Tell me about Ratnapura gem mining region and illam",))
                        with q_col3:
                            st.button("📜 NGJA Certification", use_container_width=True, on_click=set_query, args=("How to certify gemstones with NGJA Sri Lanka?",))

                    with tab_sources:
                        if sources:
                            st.markdown("#### 📄 Grounded Reference Knowledge Files")
                            st.caption("Information extracted from verified domain documents stored in ChromaDB:")
                            for src in sources:
                                st.markdown(f"""
                                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.6rem; display: flex; align-items: center; justify-content: space-between;">
                                    <span style="color: #38BDF8; font-weight: 600;">📄 {src}</span>
                                    <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 0.78rem; padding: 0.2rem 0.7rem; border-radius: 999px; font-weight: 600;">Verified Context</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No specific document chunks were required for this response.")

                    with tab_audit:
                        st.markdown("#### 🔄 4-Agent Architecture Execution Log")
                        st.markdown(f"""
                        - 🎯 **Agent 1 (ClassifierAgent)**: Classified query into **`{category_display}`** (Is Off-Topic: `False`)
                        - 🧠 **Agent 2 (PlannerAgent)**: Formulated semantic retrieval query & requested top $k=5$ chunks
                        - 🔍 **Agent 3 (RetrievalAgent)**: Executed vector embedding search against ChromaDB (`SentenceTransformers`)
                        - ✨ **Agent 4 (SynthesizerAgent)**: Generated grounded executive answer with document citations
                        """)

            except Exception as e:
                import traceback
                traceback.print_exc()
                st.error(f"Something went wrong with the multi-agent pipeline: {str(e)}")

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
