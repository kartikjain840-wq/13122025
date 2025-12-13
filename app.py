import streamlit as st
import pandas as pd
import plotly.express as px
import re
import unicodedata
from duckduckgo_search import DDGS

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Faber Nexus | AI Consultant Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CSS
# ======================================================
st.markdown("""
<style>
.stApp { background-color: #f8fafc; }
h1, h2, h3 { color: #1e3a5f; }
.stButton>button {
    background-color: #208C8D;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}
section[data-testid="stSidebar"] { background-color: #1e3a5f; color: white; }
section[data-testid="stSidebar"] label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# UTILITIES
# ======================================================
def sanitize_filename(name):
    cleaned = re.sub(r'[<>:"/\\\\|?*]', '', name)
    return unicodedata.normalize("NFKD", cleaned)

def safe_global_search(query, num_results=4):
    results = []
    try:
        with DDGS() as ddgs:
            for res in ddgs.text(query, max_results=num_results):
                snippet = res.get("body", "")
                match = re.search(
                    r'(₹\d+(?:\.\d+)?(?:\s?(?:cr|crore|lakh|lakhs))?|\d+(?:\.\d+)?%)',
                    snippet,
                    re.IGNORECASE
                )
                results.append({
                    "title": res.get("title", "Case Study"),
                    "summary": snippet,
                    "link": res.get("href", "#"),
                    "savings": match.group(0) if match else "See Report",
                    "impact": "Operational Improvement"
                })
    except Exception:
        return [{
            "title": "Offline Benchmark",
            "summary": "Live search unavailable.",
            "link": "#",
            "savings": "N/A",
            "impact": "Unavailable"
        }]
    return results

# ======================================================
# HEADER
# ======================================================
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("## 🟦 **FABER**")
with col2:
    st.title("NEXUS")
    st.caption("AI-Driven Operations Intelligence Platform | Internal Pre-Sales Tool")

st.divider()

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.header("🎯 Project Scoping")

    industry_sb = st.selectbox(
        "Select Client Industry:",
        ["Automotive", "Pharmaceuticals", "FMCG / CPG", "Healthcare", "Retail"]
    )

    tool_sb = st.selectbox(
        "Select Diagnostic Framework:",
        ["VSM", "5S", "TPM", "Lean", "Six Sigma", "Kanban"]
    )

    region_sb = st.selectbox(
        "Select Region:",
        ["India", "USA", "UK", "Germany", "France", "UAE", "Singapore", "Australia"]
    )

    budget_sb = st.select_slider(
        "💰 Client Budget:",
        ["<₹10 Cr", "₹10–50 Cr", "₹50–100 Cr", "₹100 Cr+"]
    )

    st.divider()
    st.success("Internal Archive: Online")
    st.success("Global Search: Ready")

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "🧠 Internal Brain (Archives)",
    "🌍 External Brain (Live Search)",
    "💰 ROI Simulator"
])

# ======================================================
# TAB 1 — INTERNAL BRAIN (FILTERS + CLICKABLE CARDS)
# ======================================================
with tab1:
    st.subheader("📂 Faber Archives – Delivered Impact")

    projects = [
        {
            "id": 1,
            "company": "Maruti Suzuki",
            "location": "India",
            "date": "2025-10-15",
            "summary": "Value stream mapping across assembly lines reduced waste by 28%.",
            "savings": "₹45 Cr",
            "savings_pct": "22%",
            "impact": "35%",
            "impact_label": "Time Reduced",
            "industry": "Automotive",
            "tool": "VSM",
            "duration": "4 months",
            "team": 4,
            "roles": ["Engagement Lead", "Process Expert", "Data Analyst", "Change Manager"],
            "extra": "Throughput increased by 42%"
        },
        {
            "id": 2,
            "company": "Apollo Hospitals",
            "location": "India",
            "date": "2025-09-20",
            "summary": "5S rollout across 12 OTs improved turnaround time.",
            "savings": "₹12 Cr",
            "savings_pct": "18%",
            "impact": "27%",
            "impact_label": "Time Reduced",
            "industry": "Healthcare",
            "tool": "5S",
            "duration": "2.5 months",
            "team": 3,
            "roles": ["Lean Consultant", "Healthcare Ops Expert", "Quality Lead"],
            "extra": "OT utilization up 33%"
        },
        {
            "id": 3,
            "company": "Reliance Retail",
            "location": "India",
            "date": "2025-08-10",
            "summary": "Kanban-based visual management reduced store stockouts.",
            "savings": "₹28 Cr",
            "savings_pct": "25%",
            "impact": "40%",
            "impact_label": "Time Reduced",
            "industry": "Retail",
            "tool": "Kanban",
            "duration": "3 months",
            "team": 3,
            "roles": ["Retail Ops Lead", "Supply Chain Analyst", "Implementation Lead"],
            "extra": "Sales increased by 19%"
        }
    ]

    if "selected_project" not in st.session_state:
        st.session_state.selected_project = None

    # ---------- DETAIL VIEW ----------
    if st.session_state.selected_project:
        p = st.session_state.selected_project
        if st.button("⬅ Back to Projects"):
            st.session_state.selected_project = None
            st.experimental_rerun()

        st.markdown(f"## {p['company']} — {p['location']}")
        st.caption(f"Date: {p['date']}")

        st.write(p["summary"])

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Cost Savings", p["savings"], p["savings_pct"])
        with c2:
            st.metric(p["impact_label"], p["impact"])

        st.divider()
        st.write(f"**Industry:** {p['industry']}")
        st.write(f"**Tool:** {p['tool']}")
        st.write(f"**Duration:** {p['duration']}")
        st.write(f"**Team Size:** {p['team']}")

        st.markdown("### Team Roles")
        for r in p["roles"]:
            st.write(f"- {r}")

        st.info(f"📈 {p['extra']}")

    # ---------- CARD VIEW ----------
    else:
        f1, f2 = st.columns(2)
        industry_filter = f1.selectbox(
            "Filter by Industry",
            ["All"] + sorted(set(p["industry"] for p in projects))
        )
        tool_filter = f2.selectbox(
            "Filter by Tool",
            ["All"] + sorted(set(p["tool"] for p in projects))
        )

        filtered = [
            p for p in projects
            if (industry_filter == "All" or p["industry"] == industry_filter)
            and (tool_filter == "All" or p["tool"] == tool_filter)
        ]

        cols = st.columns(3)
        for i, p in enumerate(filtered):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {p['company']}")
                    st.caption(f"{p['location']} • {p['date']}")
                    st.write(p["summary"])
                    st.divider()

                    a, b = st.columns(2)
                    a.markdown(f"### {p['savings']}")
                    a.caption("Cost Savings")
                    b.markdown(f"### {p['impact']}")
                    b.caption(p["impact_label"])

                    st.caption(f"{p['industry']} • {p['tool']}")
                    st.caption(f"⏱ {p['duration']} | 👥 {p['team']} members")

                    if st.button("View Details", key=p["id"]):
                        st.session_state.selected_project = p
                        st.experimental_rerun()

# ======================================================
# TAB 2 — EXTERNAL BRAIN
# ======================================================
with tab2:
    st.subheader("🌍 Global Benchmark Intelligence")

    query = st.text_input(
        "Search:",
        f"{industry_sb} {tool_sb} case study {region_sb}"
    )

    if st.button("Run Search"):
        st.session_state.results = safe_global_search(query)

    if "results" in st.session_state:
        for r in st.session_state.results:
            st.markdown(f"### [{r['title']}]({r['link']})")
            st.write(r["summary"])
            st.write(f"💰 {r['savings']}")
            st.divider()

# ======================================================
# TAB 3 — ROI SIMULATOR
# ======================================================
with tab3:
    st.subheader("💰 ROI Simulator")

    c1, c2 = st.columns([1, 2])
    with c1:
        revenue = st.number_input("Client Revenue (₹ Cr)", 100)
        ineff = st.slider("Inefficiency (%)", 5, 30, 15)
        fee = st.number_input("Consulting Fee (₹ Lakhs)", 25)

    with c2:
        savings = revenue * ineff / 100
        roi = (savings * 100 / fee) if fee > 0 else 0

        df = pd.DataFrame({
            "Category": ["Consulting Fee", "Projected Savings"],
            "₹ Crores": [fee / 100, savings]
        })

        fig = px.bar(df, x="Category", y="₹ Crores", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"Projected ROI: {roi:.1f}x")

# ======================================================
# FOOTER
# ======================================================
st.divider()
st.caption("Faber Infinite Consulting | Internal Tool v3.0")
