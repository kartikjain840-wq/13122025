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
    page_title="Project Intelligence Dashboard",
    page_icon="📂",
    layout="wide"
)

# ======================================================
# TEXT HELPERS (NO NLTK – CLOUD SAFE)
# ======================================================
def sentences(text):
    return [s.strip() for s in re.split(r"[.!?]\s+", text) if len(s.strip()) > 25]

def pick_sentence(text, keywords, default):
    for s in sentences(text):
        if any(k in s.lower() for k in keywords):
            return s
    return default

# ======================================================
# FILE SCANNING
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
# PROJECT ANALYSIS (RULE-BASED, STABLE)
# ======================================================
def analyze_project(text):
    industry = pick_sentence(
        text,
        ["automotive", "healthcare", "fmcg", "manufacturing", "logistics", "retail"],
        "Industry not explicitly stated"
    )

    objective = pick_sentence(
        text,
        ["objective", "aim", "goal", "challenge", "problem"],
        "Improve operational performance"
    )

    result = pick_sentence(
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
st.caption("Industry • Objectives • Results • Tools • File Reference")
st.divider()

# ======================================================
# INPUT MODE
# ======================================================
mode = st.radio(
    "Choose input method",
    ["Google Drive Folder (recommended)", "Upload Files"],
    horizontal=True
)

PROJECTS = []

# ======================================================
# MODE 1 — GOOGLE DRIVE (DEFENSIVE)
# ======================================================
if mode == "Google Drive Folder (recommended)":
    drive_link = st.text_input(
        "🔗 Google Drive Folder Link",
        help="Share folder → Anyone with link → Viewer | Only PDF/PPT/PPTX"
    )

    if st.button("📥 Load Projects from Drive") and drive_link:
        if "drive.google.com/drive/folders/" not in drive_link:
            st.error("❌ Please paste a valid Google Drive *FOLDER* link.")
        else:
            with st.spinner("Downloading files from Google Drive..."):
                try:
                    gdown.download_folder(
                        drive_link,
                        output="drive_projects",
                        quiet=True,
                        use_cookies=False
                    )
                    st.success("Files loaded successfully")
                except Exception:
                    st.error("""
❌ Google Drive blocked the download.

Fix checklist:
1. Folder access = Anyone with link → Viewer
2. Folder contains only PDF / PPT / PPTX
3. No Google Docs / Sheets / Slides
4. Try again after 1–2 minutes
""")

    if os.path.exists("drive_projects"):
        for f in scan_folder("drive_projects"):
            text = extract_text(f)
            industry, objective, result, tools = analyze_project(text)

            PROJECTS.append({
                "name": f["name"],
                "industry": industry,
                "objective": objective,
                "result": result,
                "tools": tools,
                "source": "Google Drive"
            })

# ======================================================
# MODE 2 — FILE UPLOAD (100% FAIL-PROOF)
# ======================================================
if mode == "Upload Files":
    uploads = st.file_uploader(
        "Upload PDF / PPT / PPTX files",
        type=["pdf", "ppt", "pptx"],
        accept_multiple_files=True
    )

    os.makedirs("uploads", exist_ok=True)

    for u in uploads:
        path = os.path.join("uploads", u.name)
        with open(path, "wb") as f:
            f.write(u.read())

        fobj = {"path": path, "ext": Path(path).suffix.lower()}
        text = extract_text(fobj)
        industry, objective, result, tools = analyze_project(text)

        PROJECTS.append({
            "name": u.name,
            "industry": industry,
            "objective": objective,
            "result": result,
            "tools": tools,
            "source": "Uploaded"
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
                st.caption(f"📄 Source: {p['source']}")

else:
    st.info("Load a Google Drive folder or upload files to see projects.")

st.divider()
st.caption("Consulting Project Intelligence | Streamlit Cloud Safe")
