import streamlit as st
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium Custom CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Main Background ── */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #111128 50%, #0d0d2b 100%);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e0e24 0%, #161638 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e2e8f0 !important;
    }

    /* ── Hero Title ── */
    .hero-title {
        text-align: center;
        padding: 2rem 0 0.5rem 0;
    }
    .hero-title h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #a78bfa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* ── Input Field ── */
    .stTextInput > div > div > input {
        background-color: rgba(30, 30, 60, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 0.85rem 1rem !important;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.15) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    .stTextInput label {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* ── Primary Button ── */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
        border: none !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* ── Status Expanders ── */
    details[data-testid="stExpander"] {
        background: rgba(30, 30, 60, 0.4) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 12px !important;
        margin-bottom: 0.5rem;
    }
    details[data-testid="stExpander"] summary {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    details[data-testid="stExpander"] .stMarkdown p {
        color: #cbd5e1 !important;
    }

    /* ── Status Widget ── */
    [data-testid="stStatusWidget"] {
        background: rgba(30, 30, 60, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
    }
    [data-testid="stStatusWidget"] label,
    [data-testid="stStatusWidget"] p,
    [data-testid="stStatusWidget"] span {
        color: #e2e8f0 !important;
    }

    /* ── Report Container ── */
    .report-card {
        background: linear-gradient(135deg, rgba(30, 30, 60, 0.6), rgba(20, 20, 50, 0.8));
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        color: #e2e8f0;
        line-height: 1.8;
    }
    .report-card h1, .report-card h2, .report-card h3 {
        color: #c4b5fd !important;
        margin-top: 1.5rem;
    }
    .report-card p, .report-card li {
        color: #d1d5db !important;
    }
    .report-card a {
        color: #818cf8 !important;
    }

    /* ── Critic Card ── */
    .critic-card {
        background: linear-gradient(135deg, rgba(30, 40, 50, 0.6), rgba(20, 30, 45, 0.8));
        border: 1px solid rgba(251, 191, 36, 0.25);
        border-left: 4px solid #f59e0b;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        color: #e2e8f0;
        line-height: 1.8;
    }
    .critic-card h1, .critic-card h2, .critic-card h3 {
        color: #fbbf24 !important;
    }
    .critic-card p, .critic-card li {
        color: #d1d5db !important;
    }

    /* ── Section Headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
    }
    .section-header h2 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0 !important;
        margin: 0;
    }
    .section-header .icon {
        font-size: 1.5rem;
    }

    /* ── Download Button ── */
    .stDownloadButton > button {
        background: rgba(30, 30, 60, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        color: #c4b5fd !important;
        border-radius: 12px !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        border-color: #818cf8 !important;
        color: #e2e8f0 !important;
    }

    /* ── Dividers ── */
    hr {
        border: none;
        border-top: 1px solid rgba(99, 102, 241, 0.15);
        margin: 2rem 0;
    }

    /* ── Sidebar Info Box ── */
    .sidebar-info {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1rem;
        color: #c4b5fd;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ── Step indicator pills ── */
    .step-pill {
        display: inline-block;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15));
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        color: #a5b4fc;
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    /* ── Alerts / Warnings ── */
    .stAlert {
        border-radius: 12px !important;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 500;
    }

    /* ── General text color ── */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #cbd5e1;
    }
    h1, h2, h3, h4 {
        color: #e2e8f0 !important;
    }

    /* ── Hide anchor links ── */
    .stMarkdown a.anchor-link {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("## 🧠 Research Assistant")
    st.markdown("---")
    st.markdown("""
    <div class="sidebar-info">
        <strong>Multi-Agent AI Pipeline</strong><br><br>
        🔎 <strong>Search Agent</strong> — Finds reliable sources<br>
        📖 <strong>Reader Agent</strong> — Deep-reads top URLs<br>
        ✍️ <strong>Writer Chain</strong> — Drafts full reports<br>
        ⚖️ <strong>Critic Chain</strong> — Reviews quality
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Environment status indicators
    st.markdown("#### Status")
    openai_ok = bool(os.getenv("OPENAI_API_KEY"))
    tavily_ok = bool(os.getenv("TAVILY_API_KEY"))
    
    if openai_ok:
        st.success("✅ OpenAI API Key loaded")
    else:
        st.error("❌ OpenAI API Key missing")
    
    if tavily_ok:
        st.success("✅ Tavily API Key loaded")
    else:
        st.error("❌ Tavily API Key missing")

# ── Hero Section ──
st.markdown("""
<div class="hero-title">
    <h1>Research Assistant</h1>
</div>
<p class="hero-subtitle">AI-powered multi-agent pipeline that searches, reads, writes, and critiques research reports.</p>
""", unsafe_allow_html=True)

# ── Input Area ──
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    topic = st.text_input(
        "What would you like to research?",
        placeholder="e.g. Impact of AI on healthcare in 2025..."
    )
    run_btn = st.button("🚀 Start Research", use_container_width=True)

# ── Pipeline Execution ──
if run_btn:
    if not topic:
        with col2:
            st.error("⚠️ Please enter a research topic to get started.")
    else:
        state = {}

        with col2:
            st.markdown("---")

        # Step 1: Search
        with st.status("🔎  Step 1 — Searching the web for sources...", expanded=True) as status:
            st.markdown('<span class="step-pill">AGENT: Search</span>', unsafe_allow_html=True)
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent and reliable information on the topic: {topic}")]
            })
            state["search_results"] = search_result['messages'][-1].content
            st.markdown("✅ Found relevant resources across the web.")
            with st.expander("📋 View Search Results"):
                st.markdown(state["search_results"])
            status.update(label="✅  Step 1 — Search Complete", state="complete", expanded=False)

        # Step 2: Read
        with st.status("📖  Step 2 — Deep reading top sources...", expanded=True) as status:
            st.markdown('<span class="step-pill">AGENT: Reader</span>', unsafe_allow_html=True)
            reader_agent = build_reader_agent()
            reader_prompt = (
                f"Based on the following search about {topic}, "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
            reader_result = reader_agent.invoke({
                "messages": [("user", reader_prompt)]
            })
            state['scraped_content'] = reader_result['messages'][-1].content
            st.markdown("✅ Content analyzed and key information extracted.")
            with st.expander("📋 View Scraped Content"):
                st.markdown(state['scraped_content'])
            status.update(label="✅  Step 2 — Reading Complete", state="complete", expanded=False)

        # Step 3: Write
        with st.status("✍️  Step 3 — Drafting your research report...", expanded=True) as status:
            st.markdown('<span class="step-pill">CHAIN: Writer</span>', unsafe_allow_html=True)
            research_combined = (
                f"SEARCH RESULTS: \n {state['search_results']}\n\n"
                f"DETAILED SCRAPPED CONTENT: \n {state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            st.markdown("✅ Research report drafted successfully.")
            status.update(label="✅  Step 3 — Writing Complete", state="complete", expanded=False)

        # Step 4: Critique
        with st.status("⚖️  Step 4 — Quality review in progress...", expanded=True) as status:
            st.markdown('<span class="step-pill">CHAIN: Critic</span>', unsafe_allow_html=True)
            state["feedback"] = critic_chain.invoke({
                "report": state['report']
            })
            st.markdown("✅ Quality review completed.")
            status.update(label="✅  Step 4 — Review Complete", state="complete", expanded=False)

        # ── Results ──
        st.markdown("---")

        # Report
        st.markdown("""
        <div class="section-header">
            <span class="icon">📄</span>
            <h2>Research Report</h2>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="report-card">{state["report"]}</div>', unsafe_allow_html=True)

        # Critic
        st.markdown("""
        <div class="section-header">
            <span class="icon">⚖️</span>
            <h2>Critic Review</h2>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="critic-card">{state["feedback"]}</div>', unsafe_allow_html=True)

        # Download
        st.markdown("---")
        report_text = f"# Research Report: {topic}\n\n{state['report']}\n\n---\n\n# Critic Review\n\n{state['feedback']}"
        col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
        with col_d2:
            st.download_button(
                label="⬇️  Download Full Report",
                data=report_text,
                file_name=f"research_{topic.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
