# 📊 AI Dataset Report Generator

Upload a CSV → get a **dataset summary**, **AI-generated insights**, **labeled charts**,
and **business recommendations** — all compiled into a clean, downloadable HTML report.

Built with: Streamlit · pandas · matplotlib/seaborn · the Google Gemini API.

---

## ✨ Features

- 📁 **CSV upload** — drag & drop any CSV
- 📈 **Automatic dataset summary** — shape, dtypes, missing values, duplicates, numeric & categorical stats
- 🤖 **AI-generated insights** — Gemini reads the statistical summary and writes plain-English findings
- 📊 **Auto-generated charts** — missing values, correlation heatmap, distributions, top categories
- 🧠 **AI chart explanations** — each chart gets a short, relevant explanation
- 💼 **Business recommendations** — concrete, data-grounded next steps
- ⬇️ **One-click HTML report export** — self-contained file, print-to-PDF ready

---

## 🗂 Project Structure

```
ai-dataset-report-generator/
├── app.py                     # Streamlit app (entry point)
├── src/
│   ├── data_analyzer.py       # Computes dataset summary statistics
│   ├── chart_generator.py     # Builds charts, returns base64 PNGs
│   ├── ai_engine.py           # Calls the Google Gemini API for insights/report/recommendations
│   ├── report_builder.py      # Renders the final HTML report (Jinja2)
│   └── templates/
│       └── report_template.html
├── sample_data/
│   └── sample_sales.csv       # Demo dataset, works out of the box
├── outputs/                   # Generated reports land here
├── requirements.txt
├── .env.example
└── README.md
```

Each module has one job — analysis, charts, AI, and rendering are fully decoupled,
so you can swap out any piece (e.g. a different chart library, or a different
report format) without touching the others.

---

## 🚀 Setup (VS Code)

1. **Open the folder in VS Code.**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Google API key:**
   - Copy `.env.example` to a new file named `.env`
   - Get a free key at https://aistudio.google.com/apikey
   - Paste it in: `GOOGLE_API_KEY=AIza...`

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```
   It will open at `http://localhost:8501`.

6. **Try it:** check the "use the bundled sample dataset" box, or upload your own CSV,
   then click **Generate Report**.

> No API key yet? The app still runs — the statistics and charts generate normally,
> and the AI sections show a clear message telling you how to enable them.

---

## 🧩 How it works

1. `DataAnalyzer` computes structured statistics from the uploaded CSV (shape, dtypes,
   missing values, numeric/categorical stats, correlations).
2. `ChartGenerator` builds a curated set of charts (missing values, correlation heatmap,
   distributions, top categories) and returns each as a base64 PNG.
3. `AIEngine` sends the *statistical summary* (not the raw CSV) plus the chart metadata
   to Gemini in a single request, and gets back structured JSON: summary, insights,
   per-chart explanations, and recommendations.
4. `ReportBuilder` renders everything into one self-contained HTML file via Jinja2,
   which you can open in a browser or print to PDF.

---

## 🛠 Customization ideas

- Swap `gemini-2.5-flash` for a different model in `.env` (`GEMINI_MODEL=...`)
- Add more chart types in `src/chart_generator.py`
- Add a PDF export path with `weasyprint` or `pdfkit` if you want native PDF (no browser step)
- Point `AIEngine` at a different LLM provider by rewriting just that one module

---

## 📄 License

Free to use and modify for personal or commercial projects.
