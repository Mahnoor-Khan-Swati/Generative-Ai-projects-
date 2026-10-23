"""
AI Resume & Cover Letter Generator (powered by Google Gemini)
--------------------------------------------------------------
Upload a resume, paste a job description, and get a Gemini-tailored resume
and cover letter that you can edit in the browser and download as PDF.

Run with:  streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors

from utils import extract_text_from_file, generate_tailored_content, create_pdf

# Load GEMINI_API_KEY (and optional GEMINI_MODEL) from a local .env file, if present
load_dotenv()

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
)

# Minimal ChatGPT-style styling: clean, plenty of whitespace, rounded cards
st.markdown(
    """
    <style>
        .main .block-container {
            max-width: 900px;
            padding-top: 2.5rem;
        }
        h1 {
            font-weight: 700;
        }
        .stButton>button {
            background-color: #4285F4;
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.4rem;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #3367D6;
            color: white;
        }
        .stTextArea textarea {
            border-radius: 8px;
        }
        section[data-testid="stFileUploaderDropzone"] {
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📄 AI Resume & Cover Letter Generator")
st.caption("Powered by Google Gemini — upload your resume, paste a job description, and get a tailored resume + cover letter, ready to edit and download as PDF.")

# ---------------------------------------------------------------------------
# Sidebar: API key
# ---------------------------------------------------------------------------
env_key = os.getenv("GEMINI_API_KEY", "")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

with st.sidebar:
    st.header("Settings")

    if env_key:
        st.success("API key loaded from .env file ✅")
        api_key = env_key
        with st.expander("Use a different key for this session"):
            override_key = st.text_input("Gemini API Key", type="password")
            if override_key:
                api_key = override_key
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get a free key at https://aistudio.google.com/app/apikey. Tip: put it in a .env file instead so you don't need to paste it here every time.",
        )

    st.caption(f"Model: `{model_name}`")

    st.markdown("---")
    st.markdown(
        "**How it works**\n"
        "1. Upload your resume (PDF, DOCX, or TXT)\n"
        "2. Paste the job description\n"
        "3. Click Generate\n"
        "4. Edit the results if needed\n"
        "5. Download as PDF"
    )

# ---------------------------------------------------------------------------
# Input section
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

with col2:
    job_description = st.text_area("Paste the job description", height=220, placeholder="Paste the full job posting here...")

generate_clicked = st.button("✨ Generate Tailored Resume & Cover Letter", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
if generate_clicked:
    if not api_key:
        st.warning("Please provide your Gemini API key (sidebar) or add it to a .env file.")
    elif not uploaded_file:
        st.warning("Please upload your resume file.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        try:
            with st.spinner("Reading your resume..."):
                resume_text = extract_text_from_file(uploaded_file)

            if not resume_text:
                st.error("Couldn't read any text from that file. Try a different file or paste your resume as .txt.")
            else:
                with st.spinner("Tailoring your resume and cover letter with Gemini..."):
                    client = genai.Client(api_key=api_key)
                    tailored_resume, cover_letter = generate_tailored_content(
                        client, resume_text, job_description, model=model_name
                    )
                st.session_state["tailored_resume"] = tailored_resume
                st.session_state["cover_letter"] = cover_letter
                st.success("Done! Review and edit below, then download as PDF.")
        except errors.APIError as e:
            code = getattr(e, "code", "unknown")
            if code in (401, 403):
                st.error(
                    f"Authentication failed ({code}): your Gemini API key was rejected. "
                    "Double-check you copied the full key from aistudio.google.com/app/apikey "
                    "with no extra spaces."
                )
            elif code == 429:
                st.error("Rate limit hit (429): you've sent too many requests too quickly. Wait a bit and try again.")
            else:
                st.error(f"The Gemini API returned an error ({code}): {e}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------------------------------------------------------------------------
# Results: editable + downloadable
# ---------------------------------------------------------------------------
if "tailored_resume" in st.session_state:
    st.markdown("---")
    tab1, tab2 = st.tabs(["📋 Tailored Resume", "✉️ Cover Letter"])

    with tab1:
        edited_resume = st.text_area(
            "Edit your tailored resume",
            value=st.session_state["tailored_resume"],
            height=500,
            key="resume_edit_box",
        )
        resume_pdf = create_pdf(edited_resume, title="Tailored Resume")
        st.download_button(
            "⬇️ Download Resume as PDF",
            data=resume_pdf,
            file_name="tailored_resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with tab2:
        edited_cover = st.text_area(
            "Edit your cover letter",
            value=st.session_state["cover_letter"],
            height=500,
            key="cover_edit_box",
        )
        cover_pdf = create_pdf(edited_cover, title="Cover Letter")
        st.download_button(
            "⬇️ Download Cover Letter as PDF",
            data=cover_pdf,
            file_name="cover_letter.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
else:
    st.info("Upload a resume and paste a job description above to get started.")
