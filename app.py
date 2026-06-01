"""
AI-Powered Product Strategy Assistant
Multi-Agent System for Product Managers
"""

import os
import warnings
import urllib3
import streamlit as st

# Suppress SSL warnings from the gateway's self-signed cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="AI Product Strategy Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
.main .block-container { padding-top: 1.5rem; }
h1 { color: #1B3A6B; }
h2 { color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 4px; }
h3 { color: #1B3A6B; }

/* Agent card */
.agent-card {
    background: #F8FAFB;
    border: 1px solid #DEE2E6;
    border-left: 4px solid #2E86AB;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}
.agent-card-done { border-left-color: #28A745; }
.agent-card-error { border-left-color: #DC3545; }

/* Status badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-green { background: #D4EDDA; color: #155724; }
.badge-blue  { background: #CCE5FF; color: #004085; }
.badge-gray  { background: #E2E3E5; color: #383D41; }
.badge-red   { background: #F8D7DA; color: #721C24; }

/* Metric box */
.metric-box {
    background: linear-gradient(135deg, #1B3A6B 0%, #2E86AB 100%);
    color: white;
    border-radius: 10px;
    padding: 18px 14px;
    text-align: center;
}
.metric-box .metric-value { font-size: 2rem; font-weight: 700; }
.metric-box .metric-label { font-size: 0.8rem; opacity: 0.85; margin-top: 4px; }

/* Chat bubbles */
.chat-user {
    background: #1B3A6B;
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    margin: 6px 0;
    max-width: 80%;
    float: right;
    clear: both;
}
.chat-assistant {
    background: #EBF4FA;
    color: #212529;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    margin: 6px 0;
    max-width: 85%;
    float: left;
    clear: both;
}
.chat-clearfix { clear: both; margin-bottom: 8px; }

/* Info banner */
.info-banner {
    background: linear-gradient(135deg, #EBF4FA 0%, #CCE5FF 100%);
    border: 1px solid #2E86AB;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ── Imports (after config) ───────────────────────────────────────────────────
from utils.document_processor import DocumentProcessor
from utils.pdf_generator import PDFReportGenerator
from agents.orchestrator import Orchestrator
from agents.base_agent import BaseAgent

# ── Session state init ───────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "analysis_results": {},
        "combined_data": "",
        "file_names": [],
        "analysis_done": False,
        "chat_history": [],       # list of {"role": "user"|"assistant", "content": str}
        "running": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ── Helpers ──────────────────────────────────────────────────────────────────
AGENT_META = {
    "customer_feedback":      {"icon": "👥", "label": "Customer Feedback Analysis"},
    "market_research":        {"icon": "📈", "label": "Market Research Summary"},
    "competitor_analysis":    {"icon": "🏁", "label": "Competitor Analysis"},
    "swot_analysis":          {"icon": "⚖️",  "label": "SWOT Analysis"},
    "feature_prioritization": {"icon": "🎯", "label": "Feature Prioritization"},
    "strategy_recommendations":{"icon": "🗺️", "label": "Strategic Recommendations"},
    "executive_summary":      {"icon": "📋", "label": "Executive Summary"},
}

PIPELINE_ORDER = list(AGENT_META.keys())


def _api_key_ok() -> bool:
    # Gateway is always pre-configured
    return True


def _count_words(text: str) -> int:
    return len(text.split())


def _render_result_card(key: str, content: str, expanded: bool = False):
    meta = AGENT_META[key]
    with st.expander(f"{meta['icon']} {meta['label']}", expanded=expanded):
        st.markdown(content)
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Regenerate", key=f"regen_{key}", use_container_width=True):
                _regenerate_agent(key)


def _regenerate_agent(key: str):
    if not st.session_state.combined_data:
        st.warning("No data loaded. Upload files first.")
        return
    with st.spinner(f"Regenerating {AGENT_META[key]['label']}..."):
        orch = Orchestrator()
        new_output = orch.run_single_agent(
            key,
            st.session_state.combined_data,
            st.session_state.analysis_results,
        )
        st.session_state.analysis_results[key] = new_output
    st.rerun()


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=72)
    st.title("Product Strategy AI")
    st.caption("Multi-Agent Analysis System")
    st.divider()

    # API Status
    st.subheader("🔑 API Status")
    st.success("✅ Gateway connected (gpt-4o-mini)")
    st.caption("keygateway.arshnivlabs.com")

    st.divider()

    # File upload
    st.subheader("📁 Upload Data Sources")
    st.caption("Supported: CSV, TXT, PDF, DOCX, JSON, XLSX")

    uploaded_files = st.file_uploader(
        "Drop files here",
        accept_multiple_files=True,
        type=["csv", "txt", "pdf", "docx", "json", "xlsx", "xls"],
        label_visibility="collapsed",
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) loaded")
        for f in uploaded_files:
            size_kb = len(f.getvalue()) / 1024
            st.caption(f"📄 {f.name} ({size_kb:.1f} KB)")

    st.divider()

    # Analysis options
    st.subheader("⚙️ Analysis Settings")
    run_all = st.checkbox("Run all 7 agents", value=True)
    if not run_all:
        selected_agents = st.multiselect(
            "Select agents to run",
            options=PIPELINE_ORDER,
            format_func=lambda k: f"{AGENT_META[k]['icon']} {AGENT_META[k]['label']}",
            default=PIPELINE_ORDER,
        )
    else:
        selected_agents = PIPELINE_ORDER

    st.divider()

    # Run button
    run_btn = st.button(
        "🚀 Run Analysis",
        use_container_width=True,
        type="primary",
        disabled=not (uploaded_files and _api_key_ok()),
    )

    if not uploaded_files:
        st.caption("Upload at least one data file to start.")

    # Status panel
    if st.session_state.analysis_done:
        st.divider()
        st.subheader("📊 Analysis Status")
        for key in PIPELINE_ORDER:
            if key in st.session_state.analysis_results:
                meta = AGENT_META[key]
                result = st.session_state.analysis_results[key]
                is_error = result.startswith("[Error")
                icon = "❌" if is_error else "✅"
                st.caption(f"{icon} {meta['icon']} {meta['label']}")


# ── Main Content ─────────────────────────────────────────────────────────────
st.title("🧠 AI-Powered Product Strategy Assistant")
st.markdown(
    """<div class="info-banner">
    <strong>Multi-Agent AI System</strong> — Upload your product data (sales reports, customer reviews, market research)
    and 7 specialized AI agents will analyze it from every angle, generating actionable insights and a downloadable strategy report.
    </div>""",
    unsafe_allow_html=True,
)

# ── Run Analysis ──────────────────────────────────────────────────────────────
if run_btn and uploaded_files and _api_key_ok():
    st.session_state.running = True
    st.session_state.analysis_results = {}
    st.session_state.analysis_done = False

    # Process uploaded files
    processor = DocumentProcessor()
    combined_parts = []
    file_names = []
    for uf in uploaded_files:
        uf.seek(0)
        text = processor.process(uf)
        combined_parts.append(text)
        file_names.append(uf.name)

    combined_data = "\n\n".join(combined_parts)
    # Truncate to avoid token overflow
    combined_data = DocumentProcessor.truncate(combined_data, max_chars=20000)

    st.session_state.combined_data = combined_data
    st.session_state.file_names = file_names

    # Progress UI
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    with progress_placeholder.container():
        progress_bar = st.progress(0)
        status_text = st.empty()

    results = {}

    def on_progress(key, msg, step, total):
        pct = int((step - 1) / total * 100)
        progress_bar.progress(pct)
        status_text.info(f"🤖 {msg}")

    with st.spinner("Multi-agent analysis in progress..."):
        orch = Orchestrator()
        # Filter to selected agents only
        if not run_all:
            # Temporarily filter — run full pipeline but skip non-selected
            all_results = {}
            total = len(selected_agents)
            for i, key in enumerate(PIPELINE_ORDER):
                if key not in selected_agents:
                    continue
                on_progress(key, AGENT_META[key]["label"], i + 1, len(PIPELINE_ORDER))
                prior_ctx = orch._build_context(all_results)
                try:
                    out = orch._run_agent(key, combined_data, prior_ctx)
                except Exception as e:
                    out = f"[Error: {str(e)}]"
                all_results[key] = out
            results = all_results
        else:
            results = orch.run(combined_data, progress_callback=on_progress)

    progress_bar.progress(100)
    status_text.success("✅ Analysis complete! All agents finished.")

    st.session_state.analysis_results = results
    st.session_state.analysis_done = True
    st.session_state.running = False

    import time
    time.sleep(1)
    progress_placeholder.empty()
    st.rerun()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_overview, tab_results, tab_chat, tab_report = st.tabs([
    "🏠 Overview",
    "📊 Analysis Results",
    "💬 AI Chat",
    "📄 Executive Report",
])

# ── TAB 1: Overview ───────────────────────────────────────────────────────────
with tab_overview:
    if not st.session_state.analysis_done:
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("How It Works")
            steps = [
                ("1️⃣", "Upload Data", "Upload CSV, PDF, TXT, DOCX, or JSON files containing your product data."),
                ("2️⃣", "Multi-Agent Analysis", "7 specialized AI agents analyze your data from different angles simultaneously."),
                ("3️⃣", "Insight Generation", "Agents collaborate and share findings to build richer, cross-validated insights."),
                ("4️⃣", "Strategy Report", "Download a professional PDF report with executive-ready recommendations."),
                ("5️⃣", "Interactive Chat", "Ask follow-up questions to any agent using the chat interface."),
            ]
            for icon, title, desc in steps:
                st.markdown(f"**{icon} {title}**")
                st.caption(desc)
                st.write("")

        with col_right:
            st.subheader("Agent Architecture")
            agents_info = [
                ("👥", "Customer Feedback Agent", "Sentiment analysis, pain points, satisfaction drivers"),
                ("📈", "Market Research Agent", "Revenue trends, market opportunities, regional analysis"),
                ("🏁", "Competitor Analysis Agent", "Competitive positioning, threats, white space"),
                ("⚖️", "SWOT Analysis Agent", "Synthesized strengths, weaknesses, opportunities, threats"),
                ("🎯", "Feature Prioritization", "RICE scoring, MoSCoW, product roadmap"),
                ("🗺️", "Strategy Agent", "OKRs, strategic roadmap, action plans"),
                ("📋", "Executive Report Agent", "Board-ready summary, KPIs, 90-day plan"),
            ]
            for icon, name, desc in agents_info:
                st.markdown(f"**{icon} {name}**")
                st.caption(desc)

        st.info("👈 Upload your files in the sidebar and click **Run Analysis** to begin.")
    else:
        # Show dashboard metrics
        st.subheader("📊 Analysis Dashboard")
        results = st.session_state.analysis_results
        completed = sum(1 for v in results.values() if v and not v.startswith("[Error"))
        total_words = sum(_count_words(v) for v in results.values())

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="metric-box">
                <div class="metric-value">{completed}/{len(PIPELINE_ORDER)}</div>
                <div class="metric-label">Agents Completed</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-box">
                <div class="metric-value">{total_words:,}</div>
                <div class="metric-label">Total Insights Generated</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-box">
                <div class="metric-value">{len(st.session_state.file_names)}</div>
                <div class="metric-label">Files Analyzed</div></div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""<div class="metric-box">
                <div class="metric-value">7</div>
                <div class="metric-label">AI Agent Perspectives</div></div>""", unsafe_allow_html=True)

        st.markdown("")
        st.subheader("🔍 Quick Insights Preview")

        # Show executive summary preview if available
        if "executive_summary" in results:
            with st.container():
                summary_preview = results["executive_summary"][:600]
                st.markdown(f"> {summary_preview}...")
                st.caption("📋 Full executive summary available in the Analysis Results tab")

        # Agent completion grid
        st.subheader("Agent Status")
        cols = st.columns(4)
        for i, key in enumerate(PIPELINE_ORDER):
            meta = AGENT_META[key]
            with cols[i % 4]:
                if key in results:
                    r = results[key]
                    if r.startswith("[Error"):
                        st.error(f"{meta['icon']} {meta['label']}")
                    else:
                        st.success(f"{meta['icon']} {meta['label']}")
                else:
                    st.info(f"{meta['icon']} {meta['label']}")


# ── TAB 2: Analysis Results ───────────────────────────────────────────────────
with tab_results:
    if not st.session_state.analysis_done:
        st.info("👈 Run the analysis first using the sidebar controls.")
    else:
        results = st.session_state.analysis_results
        st.subheader("Analysis Results by Agent")
        st.caption(f"Analyzed {len(st.session_state.file_names)} file(s) · {len(results)} agents completed")

        # Filter control
        filter_col, search_col = st.columns([2, 3])
        with filter_col:
            show_filter = st.selectbox(
                "Show",
                ["All Agents", "Completed Only", "Errors Only"],
                label_visibility="collapsed",
            )

        for key in PIPELINE_ORDER:
            if key not in results:
                continue
            content = results[key]
            is_error = content.startswith("[Error")
            if show_filter == "Completed Only" and is_error:
                continue
            if show_filter == "Errors Only" and not is_error:
                continue
            _render_result_card(key, content, expanded=(key == "executive_summary"))

        st.divider()
        # Re-run all button
        if st.button("🔄 Re-Run Full Analysis", type="secondary"):
            st.session_state.analysis_done = False
            st.session_state.analysis_results = {}
            st.rerun()


# ── TAB 3: Chat ───────────────────────────────────────────────────────────────
with tab_chat:
    st.subheader("💬 Chat with Your Product Data")
    st.caption(
        "Ask questions about the analysis, request deeper dives, or explore strategic options. "
        "The assistant has full context from all 7 agent analyses."
    )

    if not st.session_state.analysis_done:
        st.info("Run the analysis first to enable the chat interface with full context.")
    else:
        # Chat display
        chat_container = st.container(height=500)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div class="info-banner">
                💡 <strong>Try asking:</strong><br>
                • "What are the top 3 products I should invest in?"<br>
                • "Which region shows the most growth opportunity?"<br>
                • "What's our biggest competitive risk right now?"<br>
                • "Give me a 30-day action plan for the team."<br>
                • "Which customer segments have the lowest satisfaction?"
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(
                            f'<div class="chat-user">👤 {msg["content"]}</div>'
                            f'<div class="chat-clearfix"></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="chat-assistant">🤖 {msg["content"]}</div>'
                            f'<div class="chat-clearfix"></div>',
                            unsafe_allow_html=True
                        )

        # Chat input
        chat_col1, chat_col2 = st.columns([5, 1])
        with chat_col1:
            user_input = st.chat_input("Ask a question about your product strategy...")
        with chat_col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner("🤖 Thinking..."):
                orch = Orchestrator()
                context = orch.get_chat_context(st.session_state.analysis_results)

                chat_agent = BaseAgent(
                    name="Product Strategy Chat Agent",
                    system_prompt=(
                        "You are an expert Product Strategy Advisor with access to detailed AI analysis "
                        "of a business's products, customers, markets, and competitors. "
                        "Answer questions concisely but thoroughly, referencing specific data from the analysis. "
                        "Be strategic, data-driven, and actionable. Format responses with clear structure "
                        "using headers and bullet points where helpful. "
                        "If asked for recommendations, provide specific, prioritized actions with rationale."
                    ),
                )
                # Build conversation in Anthropic format
                api_history = []
                for msg in st.session_state.chat_history[:-1]:
                    api_history.append({"role": msg["role"], "content": msg["content"]})

                response = chat_agent.chat(
                    conversation_history=api_history,
                    user_message=user_input,
                    context=context,
                )

            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()


# ── TAB 4: Executive Report ───────────────────────────────────────────────────
with tab_report:
    st.subheader("📄 Executive Report")

    if not st.session_state.analysis_done:
        st.info("Run the analysis first to generate the executive report.")
    else:
        results = st.session_state.analysis_results

        # Preview
        st.markdown("### Report Preview")
        if "executive_summary" in results:
            st.markdown(results["executive_summary"])
        else:
            st.warning("Executive summary not available. Re-run analysis to generate it.")

        st.divider()

        # Report generation
        st.markdown("### Download Full Report")
        st.caption(
            "Generate a professionally formatted PDF report containing all 7 agent analyses, "
            "insights, strategic recommendations, and the executive summary."
        )

        report_col1, report_col2 = st.columns([2, 3])
        with report_col1:
            include_sections = st.multiselect(
                "Include sections",
                options=PIPELINE_ORDER,
                default=PIPELINE_ORDER,
                format_func=lambda k: f"{AGENT_META[k]['icon']} {AGENT_META[k]['label']}",
            )

        with report_col2:
            gen_btn = st.button("⚡ Generate PDF Report", type="primary", use_container_width=True)

        if gen_btn:
            with st.spinner("📄 Generating professional PDF report..."):
                filtered_results = {k: v for k, v in results.items() if k in include_sections}
                generator = PDFReportGenerator()
                pdf_bytes = generator.generate(
                    analysis_results=filtered_results,
                    uploaded_file_names=st.session_state.file_names,
                )

            st.success("✅ PDF report generated!")
            st.download_button(
                label="⬇️ Download Executive Report (PDF)",
                data=pdf_bytes,
                file_name="product_strategy_executive_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )

        st.divider()

        # Individual section downloads
        st.markdown("### Export Individual Sections")
        for key in PIPELINE_ORDER:
            if key in results and not results[key].startswith("[Error"):
                meta = AGENT_META[key]
                dl_col1, dl_col2 = st.columns([3, 1])
                with dl_col1:
                    st.caption(f"{meta['icon']} {meta['label']}")
                with dl_col2:
                    st.download_button(
                        label="⬇️ TXT",
                        data=results[key].encode("utf-8"),
                        file_name=f"{key}_analysis.txt",
                        mime="text/plain",
                        key=f"dl_{key}",
                        use_container_width=True,
                    )


# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    """<div style="text-align:center; color:#6C757D; font-size:0.8rem;">
    🧠 AI-Powered Product Strategy Assistant · Multi-Agent Analysis System ·
    Powered by Anthropic Claude · Built for Product Managers
    </div>""",
    unsafe_allow_html=True,
)
