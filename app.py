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

# ========================
