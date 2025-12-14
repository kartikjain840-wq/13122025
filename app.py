import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from pathlib import Path
from datetime import datetime
import gdown
import fitz  # PyMuPDF
from pptx import Presentation

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Faber Nexus | Consulting Knowledge OS",
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
.kpi {
    background: white;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# MASTER LISTS
# ======================================================
INDUSTRIES = ["Automotive", "Healthcare", "FMCG", "Manufacturing", "Logistics"]
TOOLS = ["VSM", "5S", "Lean", "TPM", "Six Sigma", "Kanban"]

# ======================================================
# SIMPLE SENTENCE TOKENIZER (CLOUD SAFE)
# ======================================================
def simple_sent_tokenize(text):
    return [s.strip() for s in re.split(r'[.!?]\s+', text) if len(s.strip()) > 20]

# ======================================================
# FILE HANDLING
# ======================================================
def scan_folder(path):
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            full = os.path.join(root, f)
            stat = os.stat(full)
            files.append({
                "title": f,
                "path": full,
                "ext": Path(f).suffix.lower(),
                "date": datetime.fromtimestamp(stat.st_mtime)
            })
    return files

def extract_text(file):
    try:
        if file["ext"] == ".pdf":
            doc = fitz.open(file["path"])
            return " ".join(p.get_text() for p in doc)[:4000]
        if file["ext"] in [".ppt", ".pptx"]:
            prs = Presentation(file["path"])
            return " ".join(
                shape.text for slide in prs.slides
                for shape in slide.shapes if hasattr(shape, "text")
            )[:4000]
    except:
        return ""
    return ""

# ======================================================
# AI-LIKE ANALYSIS (RULE BASED, STABLE)
# ======================================================
def analyze_document(text):
    if not text:
        return {
            "summary": "No readable content.",
            "problem": "Information unavailable",
            "insight": "Document could not be parsed",
            "impact": "Not quantified",
            "tools": ["General"]
        }

    sents = simple_sent_tokenize(text)
    summary = " ".join(sents[:2]) if sents else "No preview available"

    problem = next((s for s in sents if any(k in s.lower() for k in
                ["delay", "ineff", "bottleneck", "waste", "error"])), "Operational inefficiencies identified")

    insight = next((s for s in sents if any(k in s.lower() for k in
                ["analysis", "identified", "root", "revealed"])), "Process analysis highlighted improvement levers")

    impact = next((s for s in sents if any(k in s.lower() for k in
                ["reduc", "improv", "%", "increase", "saving"])), "Potential efficiency and cost improvements")

    tools = [t for t in TOOLS if t.lower() in text.lower()]
    if not tools:
        tools = ["General"]

    return {
        "summary": summary,
        "problem": problem,
        "insight": insight,
        "impact": impact,
        "tools": tools
    }

# ======================================================
# HEADER
# ======================================================
st.title("🚀 FABER NEXUS")
st.caption("Consulting Knowledge & Intelligence OS")
st.divider()

# ======================================================
# SIDEBAR — GOOGLE DRIVE
# ======================================================
with st.sidebar:
    drive_link = st.text_input(
        "🔗 Google Drive Folder Link",
        help="Set access: Anyone with link → Viewer"
    )

    if st.button("📥 Load Internal Brain") and drive_link:
        with st.spinner("Downloading files from Google Drive..."):
            gdown.download_folder(
                drive_link,
                output="internal_drive",
                quiet=True,
                use_cookies=False
            )
        st.success("Internal Brain loaded")

# ======================================================
# BUILD INTERNAL BRAIN
# ======================================================
CARDS = []
DRIVE_DIR = "internal_drive"

if os.path.exists(DRIVE_DIR):
    for f in scan_folder(DRIVE_DIR):
        text = extract_text(f)
        analysis = analyze_document(text)

        CARDS.append({
            "title": f["title"],
            "date": f["date"],
            "summary": analysis["summary"],
            "problem": analysis["problem"],
            "insight": analysis["insight"],
            "impact": analysis["impact"],
            "tools": ", ".join(analysis["tools"])
        })

# ======================================================
# KPI ROLLUPS (ACROSS ALL FILES)
# ======================================================
total_files = len(CARDS)
tool_count = pd.Series(
    ",".join(c["tools"] for c in CARDS).split(",")
).value_counts() if CARDS else pd.Series()

# ======================================================
# TABS
# ======================================================
tab1, tab2 = st.tabs(["🧠 Internal Brain", "📊 Portfolio KPIs"])

# ======================================================
# TAB 1 — INTERNAL BRAIN CARDS
# ======================================================
with tab1:
    st.subheader("📂 Internal Brain – Problem | Insight | Impact")

    cols = st.columns(3)
    for i, c in enumerate(CARDS):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {c['title']}")
                st.caption(c["date"].strftime("%d %b %Y"))
                st.write(f"**Problem:** {c['problem']}")
                st.write(f"**Insight:** {c['insight']}")
                st.write(f"**Impact:** {c['impact']}")
                st.divider()
                st.caption(f"Tools: {c['tools']}")

# ======================================================
# TAB 2 — KPI ROLLUPS
# ======================================================
with tab2:
    st.subheader("📊 Knowledge Portfolio KPIs")

    k1, k2, k3 = st.columns(3)
    k1.metric("Total Files Analysed", total_files)
    k2.metric("Distinct Tools Used", tool_count.count())
    k3.metric("Most Frequent Tool", tool_count.idxmax() if not tool_count.empty else "—")

    if not tool_count.empty:
        fig = px.bar(
            tool_count.reset_index(),
            x="index",
            y=0,
            labels={"index": "Tool", "0": "Document Count"},
            title="Tool Usage Across Knowledge Base"
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Faber Infinite Consulting | Knowledge OS")
