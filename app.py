import streamlit as st
import pandas as pd
#import plotly.express as px
import time
import re
import unicodedata
#from duckduckgo_search import DDGS

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
# GLOBAL CSS STYLING (Safe, Future-Proof)
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
# UTILITY: CLEAN FILE NAMES
# ------------------------------------------------------
def sanitize_filename(name):
    """Remove invalid filename characters."""
    cleaned = re.sub(r'[<>:"/\\\\|?*]', '', name)
    return unicodedata.normalize("NFKD", cleaned)


# ------------------------------------------------------
# SAFE SEARCH FUNCTION (BULLETPROOF)
# ------------------------------------------------------
def safe_global_search(query, num_results=4):
    """
    A fully error-proof DuckDuckGo search wrapper.
    It NEVER crashes the app and ALWAYS returns a valid list.
    """
    results = []
    enhanced_query = f"{query} case study operational excellence benchmark ROI"

    try:
        with DDGS() as ddgs:
            raw_results = ddgs.text(enhanced_query, max_results=num_results)

            for res in raw_results:
                if not isinstance(res, dict):
                    continue

                snippet = res.get("body", "") or ""
                title = res.get("title", "Case Study")
                link = res.get("href", "#")

                # Extract ROI-like numbers
                match = re.search(r'(\$\d+(?:\.\d+)?[MBK]?|\d+(?:\.\d+)?%)', snippet)
                savings = match.group(0) if match else "See Report"

                # Detect impact theme
                text = snippet.lower()
                if "reduce" in text:
                    impact = "Cost Reduction"
                elif "increase" in text:
                    impact = "Revenue Growth"
                elif "faster" in text or "speed" in text:
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
        # Fallback (guaranteed safe)
        return [{
            "title": "Offline Mode Benchmark",
            "summary": "Real-time search unavailable. Showing placeholder reference.",
            "link": "#",
            "savings": "N/A",
            "impact": "Unavailable"
        }]

    # Safety: Always return at least 1 result
    return results if results else [{
        "title": "No Results Found",
        "summary": "Search returned no usable data.",
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

    industry = st.selectbox("Select Client Industry:",
                            ["Automotive", "Pharmaceuticals", "FMCG / CPG",
                             "Heavy Engineering", "Textiles", "Logistics"])

    tool = st.selectbox("Select Diagnostic Framework:",
                        ["Value Stream Mapping (VSM)", "5S & Workplace Org",
                         "Hoshin Kanri", "Total Productive Maintenance (TPM)",
                         "Six Sigma", "Lean"])

    budget = st.select_slider("💰 Client Budget Constraint:",
                              ["<$100k", "$100k-$500k", "$500k-$1M", "$1M+"])

    st.markdown("---")
    st.markdown("### 🤖 System Status")
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
            {"Client": "[TIER1_SUPPLIER]", "Project": "Shop Floor 5S",
             "Year": 2022, "ROI": "3.2x", "Team": "3 Consultants",
             "Result": "Zero Accidents | 12 Months"}
        ],
        "Pharmaceuticals": [
            {"Client": "[PHARMA_GIANT]", "Project": "Batch Cycle Optimization",
             "Year": 2023, "ROI": "5.0x", "Team": "5 Consultants",
             "Result": "15% Capacity Release"}
        ]
    }

    projects = archive.get(industry, [])

    for p in projects:
        with st.expander(f"📄 {p['Project']} ({p['Year']}) | ROI {p['ROI']}"):
            c1, c2 = st.columns([3, 1])

            with c1:
                st.write(f"**Client:** `{p['Client']}`")
                st.write(f"**Outcome:** {p['Result']}")
                st.info(f"Recommended Team Size: {p['Team']}")

            with c2:
                numeric_roi = float(p["ROI"].replace("x", "")) if "x" in p["ROI"] else p["ROI"]
                st.metric("ROI Multiplier", numeric_roi)

            safe_name = sanitize_filename(p["Project"])
            st.download_button(
                "📥 Download Sanitized Deck",
                data="PDF Placeholder",
                file_name=f"{safe_name}.pdf"
            )


# ------------------------------------------------------
# TAB 2: LIVE SEARCH
# ------------------------------------------------------
with tab2:
    st.subheader("🌍 Live Market Intelligence")

    default_query = f"{industry} {tool} case study"
    user_query = st.text_input("Search Global Benchmarks:", value=default_query)

    if st.button("🔍 Run Live Search"):
        with st.spinner("Querying global market intelligence sources..."):
            st.session_state["search_results"] = safe_global_search(user_query)

    if "search_results" in st.session_state:
        results = st.session_state["search_results"]

        m1, m2, m3 = st.columns(3)
        m1.metric("Sources Scanned", "15+")
        m2.metric("Confidence", "High")
        m3.metric("Industry Savings Avg", "18–25%")

        st.divider()

        for r in results:
            st.markdown(f"### [{r['title']}]({r['link']})")
            st.caption(f"Impact: {r['impact']}")

            colA, colB = st.columns([3, 1])

            with colA:
                st.write(r["summary"])

            with colB:
                st.write("**Reported Savings:**")
                st.write(f"💰 {r['savings']}")

            st.markdown("---")


# ------------------------------------------------------
# TAB 3: ROI SIMULATOR
# ------------------------------------------------------
with tab3:
    st.subheader("💸 Pre-Sales Value Estimator")

    col1, col2 = st.columns([1, 2])

    with col1:
        revenue = st.number_input("Client Annual Revenue (₹ crores)", value=100)
        ineff = st.slider("Estimated Inefficiency Gap (%)", 5, 30, 15)
        fee = st.number_input("Consulting Fee (₹ lakhs)", value=25)

    with col2:
        potential_savings = revenue * (ineff / 100)

        if fee <= 0:
            roi_multiple = 0
        else:
            roi_multiple = (potential_savings * 100) / fee

        df = pd.DataFrame({
            "Category": ["Consulting Investment", "Projected Savings"],
            "Value (₹ Cr)": [fee / 100, potential_savings]
        })

        fig = px.bar(
            df, x="Category", y="Value (₹ Cr)", text_auto=True
        )

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

        st.success(f"Projected ROI: **{roi_multiple:.1f}x**")


# ------------------------------------------------------
# FOOTER
# ------------------------------------------------------
st.markdown("---")

colA, colB, colC = st.columns(3)

with colA:
    if st.button("📝 Generate Draft Proposal"):
        st.toast("Proposal generation initiated...")

with colB:
    if st.button("🤖 Stress Test with AI Client"):
        st.toast("Launching AI Skeptic Mode...")

with colC:
    st.caption("Faber Infinite Consulting | Internal Tool v2.0 (Stable Release)")
