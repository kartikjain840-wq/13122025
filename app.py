import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import re

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
    font-weight: 600;
}
.badge {
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}
.verified { background-color: #e6f9ee; color: #067647; }
.indicative { background-color: #fff4e5; color: #92400e; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# UTILITIES
# ======================================================
def relevance_score(text, keywords):
    score = 0
    text = text.lower()
    for k in keywords:
        if k.lower() in text:
            score += 2
    score += min(len(text) // 200, 3)
    return score

# ======================================================
# LIVE OPEN-SOURCE SEARCH (BEST EFFORT)
# ======================================================
def live_open_search(query, keywords, limit=6):
    SEARX_INSTANCES = [
        "https://search.disroot.org/search",
        "https://searx.tiekoetter.com/search"
    ]
    results = []

    for url in SEARX_INSTANCES:
        try:
            r = requests.get(
                url,
                params={"q": query, "format": "json", "language": "en"},
                timeout=6
            )
            data = r.json()

            for item in data.get("results", []):
                snippet = item.get("content", "") or ""
                title = item.get("title", "Case Study")

                match = re.search(
                    r'(₹\d+(?:\.\d+)?(?:\s?(?:cr|crore|lakh|lakhs))?|\d+(?:\.\d+)?%)',
                    snippet,
                    re.IGNORECASE
                )

                results.append({
                    "title": title,
                    "summary": snippet[:260] + "...",
                    "link": item.get("url", "#"),
                    "savings": match.group(0) if match else "Indicative",
                    "verified": bool(match),
                    "score": relevance_score(f"{title} {snippet}", keywords)
                })

            if results:
                break

        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]

# ======================================================
# CURATED BENCHMARK LIBRARY (ALWAYS WORKS)
# ======================================================
def curated_benchmarks(industry, tool):
    return [
        {
            "title": f"{industry} Lean Transformation Program",
            "summary": "Structured Lean deployment delivered 20–30% cost reduction and significant productivity improvement.",
            "link": "#",
            "savings": "₹30–50 Cr",
            "verified": False,
            "score": 95
        },
        {
            "title": f"{tool} Deployment Case – Multi-Plant",
            "summary": f"{tool} implementation improved throughput and reduced cycle time by 25–40%.",
            "link": "#",
            "savings": "₹15–25 Cr",
            "verified": False,
            "score": 90
        },
        {
            "title": "Operations Excellence Program – Asia",
            "summary": "End-to-end ops excellence program improved asset utilization and working capital.",
            "link": "#",
            "savings": "₹20–35 Cr",
            "verified": False,
            "score": 85
        }
    ]

# ======================================================
# HEADER
# ======================================================
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("## 🟦 **FABER**")
with col2:
    st.title("NEXUS")
    st.caption("AI-Driven Operations Intelligence Platform")

st.divider()

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.header("🎯 Project Scoping")

    industry = st.selectbox(
        "Select Client Industry",
        ["Automotive", "Healthcare", "Retail", "Pharmaceuticals", "FMCG"]
    )

    tool = st.selectbox(
        "Select Diagnostic Framework",
        ["VSM", "5S", "TPM", "Lean", "Six Sigma", "Kanban"]
    )

    region = st.selectbox(
        "Select Region",
        ["India", "USA", "UK", "Germany", "France", "UAE", "Singapore"]
    )

    search_mode = st.radio(
        "External Brain Mode",
        ["Live (Open Source)", "Curated (Guaranteed)"]
    )

    st.success("Internal Archive: Online")

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "🧠 Internal Brain",
    "🌍 External Brain",
    "💰 ROI Simulator"
])

# ======================================================
# TAB 1 — INTERNAL BRAIN (SIMPLE CARDS)
# ======================================================
with tab1:
    st.subheader("📂 Faber Archives")

    cards = [
        {"company": "Maruti Suzuki", "industry": "Automotive", "tool": "VSM",
         "summary": "Assembly line VSM reduced waste by 28%.", "savings": "₹45 Cr"},
        {"company": "Apollo Hospitals", "industry": "Healthcare", "tool": "5S",
         "summary": "5S rollout improved OT turnaround time.", "savings": "₹12 Cr"}
    ]

    f1, f2 = st.columns(2)
    ind_f = f1.selectbox("Industry Filter", ["All"] + list({c["industry"] for c in cards}))
    tool_f = f2.selectbox("Tool Filter", ["All"] + list({c["tool"] for c in cards}))

    for c in cards:
        if (ind_f == "All" or c["industry"] == ind_f) and (tool_f == "All" or c["tool"] == tool_f):
            with st.container(border=True):
                st.markdown(f"### {c['company']}")
                st.write(c["summary"])
                st.markdown(f"**Savings:** {c['savings']}")
                st.caption(f"{c['industry']} • {c['tool']}")

# ======================================================
# TAB 2 — EXTERNAL BRAIN (LIVE / CURATED TOGGLE)
# ======================================================
with tab2:
    st.subheader("🌍 External Brain – Market Intelligence")

    query = st.text_input(
        "Search",
        f"{industry} {tool} case study {region} operational excellence"
    )

    if st.button("🔍 Run Intelligence Scan"):
        keywords = [industry, tool, region, "cost", "time", "efficiency"]

        if search_mode.startswith("Live"):
            st.session_state.ext = live_open_search(query, keywords)
            if not st.session_state.ext:
                st.warning("Live sources unavailable. Showing curated benchmarks.")
                st.session_state.ext = curated_benchmarks(industry, tool)
        else:
            st.session_state.ext = curated_benchmarks(industry, tool)

    if "ext" in st.session_state:
        cols = st.columns(3)
        for i, r in enumerate(st.session_state.ext):
            with cols[i % 3]:
                with st.container(border=True):
                    badge = (
                        "<span class='badge verified'>Verified</span>"
                        if r["verified"]
                        else "<span class='badge indicative'>Indicative</span>"
                    )
                    st.markdown(badge, unsafe_allow_html=True)
                    st.markdown(f"### {r['title']}")
                    st.write(r["summary"])
                    st.divider()
                    st.markdown(f"### 💰 {r['savings']}")
                    st.caption(f"Relevance Score: {r['score']}")
                    st.markdown(f"[🔗 View Source]({r['link']})")

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
st.caption("Faber Infinite Consulting | Internal Tool v5.0")
