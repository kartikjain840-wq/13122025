import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import re
import unicodedata

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
def sanitize_filename(name):
    cleaned = re.sub(r'[<>:"/\\\\|?*]', '', name)
    return unicodedata.normalize("NFKD", cleaned)

def relevance_score(text, keywords):
    score = 0
    text = text.lower()
    for k in keywords:
        if k.lower() in text:
            score += 2
    score += min(len(text) // 200, 3)
    return score

# ======================================================
# OPEN SOURCE SEARCH (SEARXNG)
# ======================================================
def open_source_search(query, context_keywords, num_results=9):
    SEARX_URL = "https://searx.be/search"
    params = {
        "q": query,
        "format": "json",
        "language": "en",
        "categories": "general"
    }

    results = []

    try:
        r = requests.get(SEARX_URL, params=params, timeout=10)
        data = r.json()

        for item in data.get("results", []):
            snippet = item.get("content", "") or ""
            title = item.get("title", "Case Study")

            match = re.search(
                r'(₹\d+(?:\.\d+)?(?:\s?(?:cr|crore|lakh|lakhs))?|\d+(?:\.\d+)?%)',
                snippet,
                re.IGNORECASE
            )

            verified = bool(match)
            score = relevance_score(
                f"{title} {snippet}",
                context_keywords
            )

            results.append({
                "title": title,
                "summary": snippet[:280] + "...",
                "link": item.get("url", "#"),
                "savings": match.group(0) if match else "Indicative",
                "impact": "Operational Improvement",
                "verified": verified,
                "score": score
            })

    except Exception:
        return []

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:num_results]

# ======================================================
# HEADER
# ======================================================
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("## 🟦 **FABER**")
with col2:
    st.title("NEXUS")
    st.caption("AI-Driven Operations Intelligence Platform | Internal Tool")

st.divider()

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.header("🎯 Project Scoping")

    industry_sb = st.selectbox(
        "Select Client Industry:",
        ["Automotive", "Healthcare", "Retail", "Pharmaceuticals", "FMCG"]
    )

    tool_sb = st.selectbox(
        "Select Diagnostic Framework:",
        ["VSM", "5S", "TPM", "Lean", "Six Sigma", "Kanban"]
    )

    region_sb = st.selectbox(
        "Select Region:",
        ["India", "USA", "UK", "Germany", "France", "UAE", "Singapore"]
    )

    budget_sb = st.select_slider(
        "💰 Client Budget:",
        ["<₹10 Cr", "₹10–50 Cr", "₹50–100 Cr", "₹100 Cr+"]
    )

    st.success("Internal Archive: Online")
    st.success("Open-Source Search: Active")

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "🧠 Internal Brain",
    "🌍 External Brain",
    "💰 ROI Simulator"
])

# ======================================================
# TAB 1 — INTERNAL BRAIN
# ======================================================
with tab1:
    st.subheader("📂 Faber Archives – Delivered Impact")

    projects = [
        {
            "id": 1,
            "company": "Maruti Suzuki",
            "location": "India",
            "summary": "VSM across assembly lines reduced waste by 28%.",
            "savings": "₹45 Cr",
            "impact": "35%",
            "industry": "Automotive",
            "tool": "VSM",
            "duration": "4 months",
            "team": 4,
            "roles": ["Engagement Lead", "Process Expert", "Analyst", "Change Manager"]
        },
        {
            "id": 2,
            "company": "Apollo Hospitals",
            "location": "India",
            "summary": "5S rollout improved OT turnaround time significantly.",
            "savings": "₹12 Cr",
            "impact": "27%",
            "industry": "Healthcare",
            "tool": "5S",
            "duration": "2.5 months",
            "team": 3,
            "roles": ["Lean Consultant", "Ops Expert", "Quality Lead"]
        }
    ]

    f1, f2 = st.columns(2)
    ind_filter = f1.selectbox("Filter by Industry", ["All"] + sorted(set(p["industry"] for p in projects)))
    tool_filter = f2.selectbox("Filter by Tool", ["All"] + sorted(set(p["tool"] for p in projects)))

    filtered = [
        p for p in projects
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
                st.markdown(f"### 💰 {p['savings']}")
                st.caption(f"Impact: {p['impact']}")
                st.caption(f"{p['industry']} • {p['tool']}")
                st.caption(f"⏱ {p['duration']} | 👥 {p['team']} members")

# ======================================================
# TAB 2 — EXTERNAL BRAIN (OPEN SOURCE + RANKED CARDS)
# ======================================================
with tab2:
    st.subheader("🌍 External Brain – Open-Source Intelligence")

    query = st.text_input(
        "Search benchmarks",
        f"{industry_sb} {tool_sb} case study {region_sb} operational excellence"
    )

    if st.button("🔍 Run Search"):
        keywords = [industry_sb, tool_sb, region_sb, "cost", "time", "efficiency"]
        st.session_state.ext_results = open_source_search(query, keywords)

    if "ext_results" in st.session_state:
        results = st.session_state.ext_results

        if not results:
            st.warning("No results found. Try refining keywords.")
        else:
            cols = st.columns(3)
            for i, r in enumerate(results):
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
st.caption("Faber Infinite Consulting | Internal Tool v4.0")
