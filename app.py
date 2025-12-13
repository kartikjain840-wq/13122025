import streamlit as st
import pandas as pd
import plotly.express as px
import re
import unicodedata
from duckduckgo_search import DDGS

# ------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------
st.set_page_config(
    page_title="Faber Nexus | AI Consultant Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------
# GLOBAL CSS STYLING
# ------------------------------------------------------
st.markdown("""
<style>
.stApp { background-color: #f8fafc; }
h1, h2, h3 { color: #1e3a5f; font-family: 'Helvetica Neue', sans-serif; }
.stButton>button {
    background-color: #208C8D;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 0.5rem 1rem;
}
.stButton>button:hover { background-color: #1D7480; }
section[data-testid="stSidebar"] { background-color: #1e3a5f; color: white; }
section[data-testid="stSidebar"] label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# UTILITY
# ------------------------------------------------------
def sanitize_filename(name):
    cleaned = re.sub(r'[<>:"/\\\\|?*]', '', name)
    return unicodedata.normalize("NFKD", cleaned)

# ------------------------------------------------------
# SAFE GLOBAL SEARCH (₹ AWARE)
# ------------------------------------------------------
def safe_global_search(query, num_results=4):
    results = []
    enhanced_query = f"{query} case study operational excellence ROI"

    try:
        with DDGS() as ddgs:
            raw_results = ddgs.text(enhanced_query, max_results=num_results)

            for res in raw_results:
                snippet = res.get("body", "") or ""
                title = res.get("title", "Case Study")
                link = res.get("href", "#")

                # INR-aware regex
                match = re.search(
                    r'(₹\d+(?:\.\d+)?(?:\s?(?:cr|crore|lakh|lakhs))?|\d+(?:\.\d+)?%)',
                    snippet,
                    re.IGNORECASE
                )
                savings = match.group(0) if match else "See Report"

                text = snippet.lower()
                if "reduce" in text:
                    impact = "Cost Reduction"
                elif "increase" in text:
                    impact = "Revenue Growth"
                elif "faster" in text:
                    impact = "Throughput / Speed"
                else:
                    impact = "Operational Improvement"

                results.append({
                    "title": title,
                    "summary": snippet,
                    "link": link,
                    "savings": savings,
                    "impact": impact
                })

    except Exception:
        return [{
            "title": "Offline Benchmark",
            "summary": "Live search unavailable. Showing fallback data.",
            "link": "#",
            "savings": "N/A",
            "impact": "Unavailable"
        }]

    return results if results else [{
        "title": "No Results Found",
        "summary": "No usable data returned.",
        "link": "#",
        "savings": "N/A",
        "impact": "N/A"
    }]

# ------------------------------------------------------
# HEADER
# ------------------------------------------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("## 🟦 **FABER**")
with col2:
    st.title("NEXUS")
    st.caption("AI-Driven Operations Intelligence Platform | Internal Pre-Sales Tool")

st.markdown("---")

# ------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------
with st.sidebar:
    st.header("🎯 Project Scoping")

    industry = st.selectbox(
        "Select Client Industry:",
        ["Automotive", "Pharmaceuticals", "FMCG / CPG",
         "Heavy Engineering", "Textiles", "Logistics"]
    )

    tool = st.selectbox(
        "Select Diagnostic Framework:",
        ["Value Stream Mapping (VSM)", "5S & Workplace Org",
         "Hoshin Kanri", "Total Productive Maintenance (TPM)",
         "Six Sigma", "Lean"]
    )

    region = st.selectbox(
        "Select Region:",
        [
            "India",
            "United States",
            "United Kingdom",
            "Germany",
            "France",
            "UAE",
            "Singapore",
            "Australia",
            "South Africa"
        ]
    )

    budget = st.select_slider(
        "💰 Client Budget Constraint:",
        ["<₹10 Cr", "₹10–50 Cr", "₹50–100 Cr", "₹100 Cr+"]
    )

    st.markdown("---")
    st.success("Internal Archive: Online")
    st.success("Global Search: Ready")

# ------------------------------------------------------
# TABS
# ------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🧠 Internal Brain (Archives)",
    "🌍 External Brain (Live Search)",
    "💰 ROI Simulator"
])

# ------------------------------------------------------
# TAB 1: INTERNAL ARCHIVE
# ------------------------------------------------------
with tab1:
    st.subheader(f"📂 Faber Archives: {industry}")

    archive = {
        "Automotive": [
            {"Client": "[AUTO_OEM]", "Project": "Assembly Line VSM",
             "Year": 2023, "ROI": "4.5x", "Team": "4 Consultants",
             "Result": "22% Cost Reduction"},
            {"Client": "[TIER1]", "Project": "Shop Floor 5S",
             "Year": 2022, "ROI": "3.2x", "Team": "3 Consultants",
             "Result": "Zero Accidents | 12 Months"}
        ],
        "Pharmaceuticals": [
            {"Client": "[PHARMA_GIANT]", "Project": "Batch Cycle Optimization",
             "Year": 2023, "ROI": "5.0x", "Team": "5 Consultants",
             "Result": "15% Capacity Release"}
        ]
    }

    for p in archive.get(industry, []):
        with st.expander(f"📄 {p['Project']} ({p['Year']}) | ROI {p['ROI']}"):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**Client:** `{p['Client']}`")
                st.write(f"**Outcome:** {p['Result']}")
                st.info(f"Team Size: {p['Team']}")
            with c2:
                st.metric("ROI Multiplier", float(p["ROI"].replace("x", "")))

            st.download_button(
                "📥 Download Deck",
                data="PDF Placeholder",
                file_name=f"{sanitize_filename(p['Project'])}.pdf"
            )

# ------------------------------------------------------
# TAB 2: LIVE SEARCH
# ------------------------------------------------------
with tab2:
    st.subheader("🌍 Live Market Intelligence")

    default_query = f"{industry} {tool} case study {region}"
    user_query = st.text_input("Search Global Benchmarks:", value=default_query)

    if st.button("🔍 Run Live Search"):
        with st.spinner("Scanning global benchmarks..."):
            st.session_state["search_results"] = safe_global_search(user_query)

    if "search_results" in st.session_state:
        for r in st.session_state["search_results"]:
            st.markdown(f"### [{r['title']}]({r['link']})")
            st.caption(f"Impact: {r['impact']}")
            colA, colB = st.columns([3, 1])
            with colA:
                st.write(r["summary"])
            with colB:
                st.write("**Reported Savings**")
                st.write(f"💰 {r['savings']}")
            st.markdown("---")

# ------------------------------------------------------
# TAB 3: ROI SIMULATOR
# ------------------------------------------------------
with tab3:
    st.subheader("💰 Pre-Sales Value Estimator")

    c1, c2 = st.columns([1, 2])
    with c1:
        revenue = st.number_input("Client Revenue (₹ Crores)", value=100)
        ineff = st.slider("Inefficiency Gap (%)", 5, 30, 15)
        fee = st.number_input("Consulting Fee (₹ Lakhs)", value=25)

    with c2:
        savings = revenue * ineff / 100
        roi = (savings * 100 / fee) if fee > 0 else 0

        df = pd.DataFrame({
            "Category": ["Consulting Investment", "Projected Savings"],
            "Amount (₹ Cr)": [fee / 100, savings]
        })

        fig = px.bar(df, x="Category", y="Amount (₹ Cr)", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"Projected ROI: **{roi:.1f}x**")

# ------------------------------------------------------
# FOOTER
# ------------------------------------------------------
st.markdown("---")
st.caption("Faber Infinite Consulting | Internal Tool v2.1")
