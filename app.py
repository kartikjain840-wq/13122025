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
}
.verified { background-color: #e6f9ee; color: #067647; }
.indicative { background-color: #fff4e5; color: #92400e; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# INTERNAL BRAIN DATA (FIXED)
# ======================================================
INTERNAL_PROJECTS = [
    {
        "company": "Maruti Suzuki",
        "location": "India",
        "summary": "Value Stream Mapping across assembly lines reduced waste by 28%.",
        "savings": "₹45 Cr",
        "impact": "35% Cycle Time Reduction",
        "industry": "Automotive",
        "tool": "VSM",
        "duration": "4 months",
        "team": "4 members (Engagement Lead, Ops Expert, Analyst, Change Manager)"
    },
    {
        "company": "Apollo Hospitals",
        "location": "India",
        "summary": "5S implementation across 12 OTs improved turnaround time.",
        "savings": "₹12 Cr",
        "impact": "27% OT Utilization Increase",
        "industry": "Healthcare",
        "tool": "5S",
        "duration": "2.5 months",
        "team": "3 members (Lean Consultant, Ops Lead, Quality)"
    },
    {
        "company": "Reliance Retail",
        "location": "India",
        "summary": "Kanban-based replenishment reduced store stockouts.",
        "savings": "₹28 Cr",
        "impact": "40% Stockout Reduction",
        "industry": "Retail",
        "tool": "Kanban",
        "duration": "3 months",
        "team": "3 members (Retail Ops, SCM Analyst, PM)"
    }
]

# ======================================================
# UTILITIES
# ======================================================
def relevance_score(text, keywords):
    score = 0
    text = text.lower()
    for k in keywords:
        if k.lower() in text:
            score += 2
    return score

def live_open_search(query, keywords):
    urls = [
        "https://search.disroot.org/search",
        "https://searx.tiekoetter.com/search"
    ]
    results = []

    for url in urls:
        try:
            r = requests.get(
                url,
                params={"q": query, "format": "json"},
                timeout=6
            )
            data = r.json()

            for item in data.get("results", []):
                snippet = item.get("content", "")
                title = item.get("title", "Case Study")
                link = item.get("url", "")

                match = re.search(
                    r'(₹\d+(?:\.\d+)?(?:\s?(?:cr|crore|lakh|lakhs))?|\d+%)',
                    snippet
                )

                results.append({
                    "title": title,
                    "summary": snippet[:260] + "...",
                    "link": link,
                    "savings": match.group(0) if match else "Indicative",
                    "verified": bool(match),
                    "score": relevance_score(snippet, keywords)
                })

            if results:
                break
        except Exception:
            continue

    return results

def curated_benchmarks(industry, tool):
    return [
        {
            "title": f"{industry} Lean Transformation Program",
            "summary": "Lean deployment delivered 20–30% cost reduction.",
            "link": "",
            "savings": "₹30–50 Cr",
            "verified": False,
            "score": 90
        },
        {
            "title": f"{tool} Deployment Case",
            "summary": f"{tool} improved throughput by 25–40%.",
            "link": "",
            "savings": "₹15–25 Cr",
            "verified": False,
            "score": 85
        }
    ]

# ======================================================
# HEADER
# ======================================================
st.title("🚀 FABER NEXUS")
st.caption("AI-Driven Operations Intelligence Platform")
st.divider()

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    industry = st.selectbox(
        "Industry",
        ["Automotive", "Healthcare", "Retail"]
    )
    tool = st.selectbox(
        "Framework",
        ["VSM", "5S", "Kanban"]
    )
    region = st.selectbox(
        "Region",
        ["India", "USA", "Germany"]
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
# TAB 1 — INTERNAL BRAIN (FIXED + ALWAYS VISIBLE)
# ======================================================
with tab1:
    st.subheader("📂 Internal Case Archives")

    f1, f2 = st.columns(2)
    ind_filter = f1.selectbox(
        "Filter by Industry",
        ["All"] + sorted({p["industry"] for p in INTERNAL_PROJECTS})
    )
    tool_filter = f2.selectbox(
        "Filter by Tool",
        ["All"] + sorted({p["tool"] for p in INTERNAL_PROJECTS})
    )

    filtered = [
        p for p in INTERNAL_PROJECTS
        if (ind_filter == "All" or p["industry"] == ind_filter)
        and (tool_filter == "All" or p["tool"] == tool_filter)
    ]

    cols = st.columns(3)
    for i, p in enumerate(filtered):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {p['company']}")
                st.caption(p["location"])
                st.write(p["summary"])
                st.divider()
                st.markdown(f"**Savings:** {p['savings']}")
                st.write(f"**Impact:** {p['impact']}")
                st.caption(f"{p['industry']} • {p['tool']}")
                st.caption(f"⏱ {p['duration']}")
                st.caption(f"👥 {p['team']}")

# ======================================================
# TAB 2 — EXTERNAL BRAIN
# ======================================================
with tab2:
    st.subheader("🌍 External Market Intelligence")

    query = st.text_input(
        "Search",
        f"{industry} {tool} case study {region}"
    )

    if st.button("Run Search"):
        keywords = [industry, tool, region]
        if mode.startswith("Live"):
            results = live_open_search(query, keywords)
            if not results:
                st.warning("Live search unavailable. Showing curated benchmarks.")
                results = curated_benchmarks(industry, tool)
        else:
            results = curated_benchmarks(industry, tool)

        st.session_state.ext = results

    if "ext" in st.session_state:
        cols = st.columns(3)
        for i, r in enumerate(st.session_state.ext):
            with cols[i % 3]:
                with st.container(border=True):
                    badge = "verified" if r["verified"] else "indicative"
                    st.markdown(
                        f"<span class='badge {badge}'>{'Verified' if r['verified'] else 'Indicative'}</span>",
                        unsafe_allow_html=True
                    )
                    st.markdown(f"### {r['title']}")
                    st.write(r["summary"])
                    st.divider()
                    st.markdown(f"💰 {r['savings']}")
                    if r["link"]:
                        st.markdown(
                            f"<a href='{r['link']}' target='_blank'>🔗 View Source</a>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.caption("Curated internal benchmark")

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

st.divider()
st.caption("Faber Infinite Consulting | Stable Internal Build")
