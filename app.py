import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
from datetime import datetime
import gdown
import fitz  # PyMuPDF
from pptx import Presentation
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

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
# MASTER LISTS
# ======================================================
INDUSTRIES = [
    "Automotive", "Pharmaceuticals", "FMCG / CPG", "Heavy Engineering",
    "Textiles", "Logistics", "Healthcare", "Retail"
]

TOOLS = [
    "Value Stream Mapping (VSM)", "5S", "Lean", "TPM",
    "Six Sigma", "Kanban"
]

REGIONS = [
    "India", "United States", "United Kingdom", "Germany",
    "UAE", "Singapore"
]

# ======================================================
# INTERNAL CASES (SEED DATA)
# ======================================================
INTERNAL_CASES = [
    {
        "type": "case",
        "title": "Maruti Suzuki – Assembly VSM",
        "summary": "VSM reduced waste and rework across assembly lines.",
        "industry": "Automotive",
        "tool": "VSM",
        "date": datetime(2024, 10, 15),
        "impact": "35% Cycle Time Reduction",
        "savings": "₹45 Cr"
    }
]

# ======================================================
# FILE SCANNING
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
            return " ".join(p.get_text() for p in doc)[:3000]
        if file["ext"] in [".ppt", ".pptx"]:
            prs = Presentation(file["path"])
            return " ".join(
                shape.text for slide in prs.slides
                for shape in slide.shapes if hasattr(shape, "text")
            )[:3000]
    except:
        return ""
    return ""

def ai_summary_and_tags(text):
    if not text:
        return "No preview available", ["General"]

    sents = sent_tokenize(text)
    summary = " ".join(sents[:2])
    tags = []

    t = text.lower()
    for k in ["vsm", "5s", "lean", "tpm", "six sigma", "kanban"]:
        if k in t:
            tags.append(k.upper())

    return summary, tags if tags else ["General"]

# ======================================================
# HEADER
# ======================================================
st.title("🚀 FABER NEXUS")
st.caption("Consulting Knowledge & Intelligence OS")
st.divider()

# ======================================================
# SIDEBAR — GOOGLE DRIVE INPUT
# ======================================================
with st.sidebar:
    industry = st.selectbox("Industry", INDUSTRIES)
    tool = st.selectbox("Framework", TOOLS)
    region = st.selectbox("Region", REGIONS)

    drive_link = st.text_input(
        "🔗 Google Drive Folder Link",
        help="Set access to: Anyone with link → Viewer"
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
FILE_CARDS = []
DRIVE_DIR = "internal_drive"

if os.path.exists(DRIVE_DIR):
    for f in scan_folder(DRIVE_DIR):
        text = extract_text(f)
        summary, tags = ai_summary_and_tags(text)

        FILE_CARDS.append({
            "type": "file",
            "title": f["title"],
            "summary": summary,
            "industry": "Internal",
            "tool": ", ".join(tags),
            "date": f["date"],
            "impact": "Document Insight",
            "savings": "—"
        })

ALL_INTERNAL = sorted(
    INTERNAL_CASES + FILE_CARDS,
    key=lambda x: x["date"],
    reverse=True
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
# TAB 1 — INTERNAL BRAIN
# ======================================================
with tab1:
    st.subheader("📂 Internal Brain")

    cols = st.columns(3)
    for i, c in enumerate(ALL_INTERNAL):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {c['title']}")
                st.caption(c["date"].strftime("%d %b %Y"))
                st.write(c["summary"])
                st.divider()
                st.markdown(f"**Impact:** {c['impact']}")
                st.markdown(f"**Savings:** {c['savings']}")
                st.caption(f"{c['industry']} • {c['tool']}")

# ======================================================
# TAB 2 — EXTERNAL BRAIN (CURATED)
# ======================================================
with tab2:
    st.subheader("🌍 External Intelligence")
    st.info("Curated benchmark cases (static demo)")

# ======================================================
# TAB 3 — ROI SIMULATOR
# ======================================================
with tab3:
    st.subheader("💰 ROI Simulator")

    revenue = st.number_input("Client Revenue (₹ Cr)", 100)
    ineff = st.slider("Inefficiency (%)", 5, 30, 15)
    fee = st.number_input("Consulting Fee (₹ Lakhs)", 25)

    savings = revenue * ineff / 100
    roi = (savings * 100 / fee) if fee > 0 else 0

    df = pd.DataFrame({
        "Category": ["Consulting Fee", "Projected Savings"],
        "₹ Crores": [fee / 100, savings]
    })

    fig = px.bar(df, x="Category", y="₹ Crores", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    st.success(f"Projected ROI: {roi:.1f}x")

st.divider()
st.caption("Faber Infinite Consulting | Knowledge OS")
