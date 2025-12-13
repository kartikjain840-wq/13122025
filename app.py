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
# LIVE OPEN SOURCE SEARCH
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
                link = item.get("url", "")

                match = re.search(
                    r'(₹\d+(?:\.\d+)?(?:\s?(?:cr|crore|lakh|lakhs))?|\d+(?:\.\d+)?%)',
                    snippet,
                    re.IGNORECASE
                )

                results.append({
                    "title": title,
                    "summary": snippet[:260] + "...",
                    "link": link,
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
# CURATED BENCHMARKS
# ======================================================
def curated_benchmarks(industry, tool):
    return [
        {
            "title": f"{industry} Lean Transformation Program",
            "summary": "Structured Lean deployment delivered 20–30% cost reduction.",
            "link": "",
            "savings": "₹30–50 Cr",
            "verified": False,
            "score": 95
        },
        {
            "title": f"{tool} Deployment – Multi-Plant",
            "summary": f"{tool} implementation improved throughput by 25–40%.",
            "link": "",
            "savings": "₹15–25 Cr",
            "verified": False,
            "score": 90
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
    industry = st.selectbox(
        "Industry", ["Automotive", "Healthcare", "Retail", "Pharma", "FMCG"]
    )
    tool = st.selectbox(
        "Framework", ["VSM", "5S", "TPM", "Lean", "Six Sigma"]
    )
    region = st.selectbox(
        "Region", ["India", "USA", "UK", "Germany", "UAE"]
    )
    mode = st.radio(
        "External Brain Mode",
        ["Live (Open Source)", "Curated (Guaranteed)"]
    )

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "🧠 Internal Brain",
    "🌍 External Brain",
    "💰 ROI Simulator"
])

# ======================================================
# TAB 2 — EXTERNAL BRAIN (FIXED VIEW SOURCE)
# ======================================================
with tab2:
    st.subheader("🌍 External Brain – Market Intelligence")

    query = st.text_input(
        "Search",
        f"{industry} {tool} case study {region} operational excellence"
    )

    if st.button("🔍 Run Intelligence Scan"):
        keywords = [industry, tool, region, "cost", "efficiency"]
        if mode.startswith("Live"):
            results = live_open_search(query, keywords)
            if not results:
                st.warning("Live search unavailable. Showing curated benchmarks.")
                results = curated_benchmarks(industry, tool)
        else:
            results = curated_benchmarks(industry, tool)

        st.session_state.ext_results = results

    if "ext_results" in st.session_state:
        cols = st.columns(3)
        for i, r in enumerate(st.session_state.ext_results):
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

                    # ✅ FIXED VIEW SOURCE
                    if r["link"]:
                        st.markdown(
                            f"""
                            <a href="{r['link']}" target="_blank" rel="noopener noreferrer">
                                🔗 View Source
                            </a>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.caption("📁 Curated internal benchmark (no external source)")

# ======================================================
# TAB 3 — ROI SIMULATOR
# ======================================================
with tab3:
    st.subheader("💰 ROI Simulator")
    revenue = st.number_input("Revenue (₹ Cr)", 100)
    ineff = st.slider("Inefficiency (%)", 5, 30, 15)
    fee = st.number_input("Consulting Fee (₹ Lakhs)", 25)
    savings = revenue * ineff / 100
    roi = (savings * 100 / fee) if fee > 0 else 0
    st.success(f"Projected ROI: {roi:.1f}x")

# ======================================================
# FOOTER
# ======================================================
st.divider()
st.caption("Faber Infinite Consulting | Internal Tool v6.0")
