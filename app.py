import streamlit as st
import os
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from pptx import Presentation
import nltk
from nltk.tokenize import sent_tokenize
import webbrowser

# ------------------ NLTK SETUP ------------------
nltk.download("punkt")

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Faber Nexus | Internal Knowledge OS",
    page_icon="📂",
    layout="wide"
)

# =================================================
# INTERNAL STATIC PROJECTS
# =================================================
INTERNAL_PROJECTS = [
    {
        "type": "case",
        "title": "Maruti Suzuki – VSM Transformation",
        "summary": "Value stream mapping reduced waste by 28% across assembly lines.",
        "industry": "Automotive",
        "tool": "VSM",
        "date": datetime(2024, 10, 12),
        "source": "Internal Case"
    },
    {
        "type": "case",
        "title": "Apollo Hospitals – 5S Rollout",
        "summary": "5S implementation improved OT turnaround time by 27%.",
        "industry": "Healthcare",
        "tool": "5S",
        "date": datetime(2024, 9, 20),
        "source": "Internal Case"
    }
]

# =================================================
# FILE SCANNING
# =================================================
def scan_folder(folder_path):
    files = []
    for root, _, filenames in os.walk(folder_path):
        for f in filenames:
            path = os.path.join(root, f)
            stat = os.stat(path)
            files.append({
                "type": "file",
                "title": f,
                "path": path,
                "extension": Path(f).suffix.lower(),
                "date": datetime.fromtimestamp(stat.st_mtime)
            })
    return files

# =================================================
# FILE CONTENT EXTRACTION
# =================================================
def extract_text(file):
    ext = file["extension"]
    path = file["path"]

    try:
        if ext == ".pdf":
            doc = fitz.open(path)
            return " ".join(page.get_text() for page in doc)[:3000]

        if ext in [".ppt", ".pptx"]:
            prs = Presentation(path)
            text = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + " "
            return text[:3000]
    except:
        return ""

    return ""

# =================================================
# AI-STYLE AUTO SUMMARY + TAGGING (LOCAL)
# =================================================
def ai_summary_and_tags(text):
    if not text:
        return "No preview available", ["Unclassified"]

    sentences = sent_tokenize(text)
    summary = " ".join(sentences[:2])

    tags = []
    text_l = text.lower()

    if "vsm" in text_l: tags.append("VSM")
    if "5s" in text_l: tags.append("5S")
    if "lean" in text_l: tags.append("Lean")
    if "tpm" in text_l: tags.append("TPM")
    if "six sigma" in text_l: tags.append("Six Sigma")

    return summary, tags if tags else ["General"]

# =================================================
# UI — FOLDER INPUT
# =================================================
st.title("📂 FABER NEXUS — Internal Knowledge OS")
st.caption("Consulting Knowledge Base | Local + Drive")

folder_path = st.text_input(
    "📁 Enter folder path to scan",
    value=r"D:\IIM Ranchi Sem 5\VLP Faber Infinite Consulting\Week 2 Updates"
)

# =================================================
# BUILD KNOWLEDGE BASE
# =================================================
file_cards = []
if folder_path and os.path.exists(folder_path):
    raw_files = scan_folder(folder_path)

    for f in raw_files:
        text = extract_text(f)
        summary, tags = ai_summary_and_tags(text)

        file_cards.append({
            "type": "file",
            "title": f["title"],
            "summary": summary,
            "tags": tags,
            "date": f["date"],
            "path": f["path"],
            "extension": f["extension"]
        })

# Merge + sort
ALL_ITEMS = INTERNAL_PROJECTS + file_cards
ALL_ITEMS.sort(key=lambda x: x["date"], reverse=True)

# =================================================
# DISPLAY CARDS
# =================================================
st.subheader("📚 Internal Brain (Cases + Documents)")

cols = st.columns(3)

for i, item in enumerate(ALL_ITEMS):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"### {item['title']}")
            st.caption(item["date"].strftime("%d %b %Y"))

            st.write(item["summary"])

            if item["type"] == "file":
                st.caption("Tags: " + ", ".join(item["tags"]))

                # ---- FILE ACTIONS ----
                c1, c2 = st.columns(2)

                with c1:
                    if st.button("📂 Open File", key=item["path"]):
                        os.startfile(item["path"])

                with c2:
                    if item["extension"] == ".pdf":
                        st.download_button(
                            "👁 Preview PDF",
                            open(item["path"], "rb"),
                            file_name=item["title"]
                        )

            else:
                st.caption(item["source"])
