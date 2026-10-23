"""
AI Dataset Report Generator
============================
Upload a CSV -> get a statistical summary, AI-written insights,
labeled charts, and business recommendations, exportable as a
single self-contained HTML report.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.ai_engine import AIEngine
from src.chart_generator import ChartGenerator
from src.data_analyzer import DataAnalyzer
from src.report_builder import ReportBuilder

load_dotenv()

OUTPUT_DIR = Path(__file__).parent / "outputs"

st.set_page_config(page_title="AI Dataset Report Generator", page_icon="📊", layout="wide")


def load_csv(uploaded_file) -> pd.DataFrame | None:
    try:
        return pd.read_csv(uploaded_file)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Could not read this CSV: {exc}")
        return None


def render_sidebar() -> str:
    st.sidebar.header("⚙️ Settings")
    api_key_present = bool(os.environ.get("GOOGLE_API_KEY"))
    if api_key_present:
        st.sidebar.success("GOOGLE_API_KEY loaded from .env")
    else:
        st.sidebar.warning(
            "No GOOGLE_API_KEY found.\n\nCopy `.env.example` to `.env` and add your key "
            "(from https://aistudio.google.com/apikey) to enable AI-generated insights."
        )
    model = st.sidebar.text_input(
        "Model",
        value=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        help="Gemini model ID used to generate the report content.",
    )
    st.sidebar.divider()
    st.sidebar.caption(
        "Built with Streamlit + pandas + matplotlib + the Google Gemini API. "
        "Nothing you upload leaves your machine except the statistical summary "
        "sent to Gemini for narrative generation."
    )
    return model


def main():
    st.title("📊 AI Dataset Report Generator")
    st.caption("Upload a CSV → get a summary, AI insights, labeled charts, and business recommendations.")

    model = render_sidebar()

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    use_sample = st.checkbox("...or use the bundled sample dataset (sample_data/sample_sales.csv)")

    df = None
    dataset_name = ""

    if uploaded_file is not None:
        df = load_csv(uploaded_file)
        dataset_name = uploaded_file.name
    elif use_sample:
        sample_path = Path(__file__).parent / "sample_data" / "sample_sales.csv"
        df = pd.read_csv(sample_path)
        dataset_name = "sample_sales.csv"

    if df is None:
        st.info("Upload a CSV file (or check the sample dataset box) to get started.")
        return

    st.subheader("Preview")
    st.dataframe(df.head(20), use_container_width=True)
    st.caption(f"{df.shape[0]} rows × {df.shape[1]} columns")

    if st.button("🚀 Generate Report", type="primary"):
        with st.spinner("Analyzing dataset..."):
            summary = DataAnalyzer(df).analyze()

        with st.spinner("Building charts..."):
            charts = ChartGenerator(df).generate_all()
            chart_metadata = [{"title": c.title, "kind": c.kind, "column": c.column} for c in charts]

        with st.spinner("Asking Gemini for insights, explanations & recommendations..."):
            ai_content = AIEngine(model=model).generate_report_content(summary.to_dict(), chart_metadata)

        st.success("Report generated!")

        # --- On-screen results ---
        st.header("Executive Summary")
        st.write(ai_content.summary)
        if ai_content.raw_error:
            st.warning(f"AI generation note: {ai_content.raw_error}")

        st.header("Key Insights")
        for insight in ai_content.insights:
            st.markdown(f"- {insight}")

        st.header("Charts")
        cols = st.columns(2)
        for i, chart in enumerate(charts):
            with cols[i % 2]:
                st.image(
                    f"data:image/png;base64,{chart.image_base64}",
                    caption=chart.title,
                    use_container_width=True,
                )
                st.caption(ai_content.chart_explanations.get(chart.title, ""))

        st.header("Business Recommendations")
        for rec in ai_content.recommendations:
            st.markdown(f"- {rec}")

        # --- Build downloadable HTML report ---
        output_path = OUTPUT_DIR / f"{Path(dataset_name).stem}_report.html"
        ReportBuilder().render_to_file(output_path, dataset_name, summary, charts, ai_content)

        with open(output_path, "rb") as f:
            st.download_button(
                "⬇️ Download Full HTML Report",
                data=f,
                file_name=output_path.name,
                mime="text/html",
            )
        st.caption("Tip: open the downloaded HTML and use your browser's Print → Save as PDF to get a PDF version.")


if __name__ == "__main__":
    main()
