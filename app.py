import streamlit as st
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
    page_title="Faber Nexus | Project Intelligence",
    page_icon="📂",
    layout="wide"
)

# ======================================================
# SIMPLE TEXT HELPERS (CLOUD SAFE)
# ======================================================
def simple_sentences(text):
    return [s.strip() for s in re.split(r"[.!?]\s+", text) if len(s.strip()) > 20]

def find_first(text, keywords, default):
    for s in simple_sentences(text):
        if any(k in s.lower() for k in keywords):
            return s
    return default

# ======================================================
# FILE SCAN + TEXT EXTRACTION
# ======================================================
def scan_folder(path):
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            full = os.path.join(root, f)
            files.append({
                "name": f,
                "path": full,
                "ext": Path(f).suffix.lower(),
                "date": datetime.fromtimestamp(os.stat(full).st_mtime)
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
# PROJECT INTELLIGENCE (RULE BASED)
# ======================================================
def analyze_project(text):
    industry = find_first(
        text,
        ["automotive", "healthcare", "fmcg", "manufacturing", "logistics", "retail"],
        "Industry not specified"
    )

    objective = find_first(
        text,
        ["objective", "aim", "goal", "challenge", "problem"],
        "Improve operational performance"
    )

    result = find_first(
        text,
        ["reduc", "improv", "increase", "%", "saving", "impact"],
        "Operational improvements achieved"
    )

    tools = []
    for t in ["vsm", "5s", "lean", "six sigma", "tpm", "kanban"]:
        if t in text.lower():
            tools.append(t.upper())

    if not tools:
        tools = ["General"]

    return industry, objective, result, ", ".join(tools)

# ======================================================
# HEADER
# ======================================================
st.title("📂 Project Intelligence Dashboard")
st.caption("Industry | Objectives | Results | Tools | File Reference")
st.divider()

# ======================================================
# GOOGLE DRIVE INPUT
# ======================================================
drive_link = st.text_input(
    "🔗 Paste Google Drive Folder Link (Viewer access)",
    help="Right click folder → Get link → Anyone with link → Viewer"
)

if st.button("📥 Load Projects") and drive_link:
    with st.spinner("Loading files from Google Drive..."):
        gdown.download_folder(
            drive_link,
            output="drive_projects",
            quiet=True,
            use_cookies=False
        )
    st.success("Projects loaded successfully")

# ======================================================
# BUILD PROJECT CARDS
# ======================================================
PROJECTS = []
DRIVE_DIR = "drive_projects"

if os.path.exists(DRIVE_DIR):
    for f in scan_folder(DRIVE_DIR):
        text = extract_text(f)
        industry, objective, result, tools = analyze_project(text)

        PROJECTS.append({
            "name": f["name"],
            "industry": industry,
            "objective": objective,
            "result": result,
            "tools": tools,
            "path": f["path"]
        })

# ======================================================
# DISPLAY PROJECT CARDS
# ======================================================
if PROJECTS:
    cols = st.columns(3)

    for i, p in enumerate(PROJECTS):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {p['name']}")
                st.markdown(f"**Industry:** {p['industry']}")
                st.markdown(f"**Objectives:** {p['objective']}")
                st.markdown(f"**Results:** {p['result']}")
                st.markdown(f"**Tool Used:** {p['tools']}")
                st.caption(f"📄 File reference: `{p['name']}`")

else:
    st.info("Load a Google Drive folder to see projects.")

st.divider()
st.caption("Faber Infinite Consulting | Project Intelligence System")
