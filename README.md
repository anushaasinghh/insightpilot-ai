# 🧠 InsightPilot AI

![CI](https://github.com/anushaasinghh/insightpilot-ai/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

> **Upload any CSV or Excel file and get AI-powered business insights,
> interactive charts, and a downloadable PDF report — in under 90 seconds.**
> No data team. No SQL. No setup.

## 🔗 [Live App](https://insightpilot-ai-data-analysis.streamlit.app/) · [PM Documentation](pm/) · [Sprint History](agile/) · [Test Suite](qa/)

---

## 📸 Screenshots

> Upload page → auto profile → charts → AI insights → PDF export

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📁 **Upload & Profile** | CSV or Excel. Auto-cleans column names, detects types, shows missing %, duplicates, memory |
| 📊 **Auto Charts** | 5 chart types generated automatically — time series, bar, distribution, pie, heatmap |
| 🛠️ **Custom Chart Builder** | Pick any columns, any chart type, any color grouping |
| 🤖 **AI Insights** | One click → 5 ranked business insights powered by Google Gemini |
| 💬 **Natural Language Q&A** | Ask "what is my best product?" and get a specific answer |
| 📄 **PDF Report** | Download a complete report with profile, stats, and AI insights |

---

## 🗂️ Full Project Lifecycle

This project was built following a complete product development lifecycle —
not just the engineering side.

| Layer | What's included | Location |
|-------|----------------|----------|
| **Product Management** | PRD, user research, personas, competitive analysis, RICE prioritisation | [`pm/`](pm/) |
| **Agile** | 3 sprint plans, daily standups, retrospectives, definition of done | [`agile/`](agile/) |
| **Engineering** | Python, Streamlit, Gemini API, Plotly, FPDF2 | [`utils/`](utils/), [`pages/`](pages/) |
| **QA** | 29 unit tests, test plan, 12 manual test cases | [`qa/`](qa/) |
| **CI/CD** | GitHub Actions — auto-runs tests on every push | [`.github/workflows/`](.github/workflows/) |
| **Deployment** | Streamlit Cloud — free, live public URL | [Live App](YOUR_STREAMLIT_URL_HERE) |

---

## 🏗️ Project Structure

```
insightpilot-ai/
├── app.py                        # Main landing page
├── pages/
│   ├── 1_upload.py               # Upload + data profiling
│   ├── 2_visualise.py            # Auto charts + custom builder
│   ├── 3_ask_ai.py               # AI insights + Q&A chat
│   └── 4_report.py               # PDF export
├── utils/
│   ├── data_processor.py         # Load, clean, profile data
│   ├── chart_builder.py          # Plotly chart generation
│   ├── ai_analyst.py             # Gemini API integration
│   └── pdf_generator.py          # PDF report generation
├── pm/
│   ├── PRD.md                    # Product Requirements Document
│   ├── user_research.md          # Personas + interview findings
│   ├── competitive_analysis.md   # Market positioning
│   └── prioritisation.md         # RICE scoring
├── agile/
│   ├── sprint_1.md               # Sprint 1 plan + retro
│   ├── sprint_2.md               # Sprint 2 plan + retro
│   ├── sprint_3.md               # Sprint 3 plan + retro
│   └── definition_of_done.md     # Team standards
├── qa/
│   ├── test_plan.md              # QA strategy
│   ├── test_cases.md             # 12 manual test cases
│   └── tests/
│       ├── test_data_processor.py
│       ├── test_chart_builder.py
│       └── test_ai_analyst.py
├── sample_data/
│   └── sample_sales.csv          # Built-in demo dataset
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI pipeline
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/anushaasinghh/insightpilot-ai.git
cd insightpilot-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your free Gemini API key
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-key-here"
```
Get a free key (no credit card) at 👉 https://aistudio.google.com/app/apikey

### 4. Run
```bash
streamlit run app.py
```

Open http://localhost:8501

---

## 🧪 Run Tests

```bash
pip install pytest
pytest qa/tests/ -v
```

Expected output:
```
qa/tests/test_data_processor.py::test_clean_strips_column_whitespace PASSED
qa/tests/test_chart_builder.py::test_auto_charts_returns_list PASSED
qa/tests/test_ai_analyst.py::test_parse_insights_valid_json PASSED
...
29 passed in 1.8s
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend + Backend | Streamlit | UI and app logic |
| AI | Google Gemini 1.5 Flash | Insights + Q&A |
| Data | Pandas, NumPy | Processing + analysis |
| Charts | Plotly | Interactive visualisations |
| PDF | FPDF2 | Report generation |
| Testing | pytest | Unit tests |
| CI/CD | GitHub Actions | Automated test pipeline |
| Deployment | Streamlit Cloud | Free hosting |

---

## 📋 PM Documentation Highlights

### Problem Statement
Non-technical business users have data but no fast way to extract insights.
Existing tools are too complex, too expensive, or require a data team.

### Target Users
- Marketing managers who need campaign performance insights
- Operations analysts who produce weekly reports manually
- Founders and growth leads who need instant "so what" from their data

### North Star Metric
**Time-to-first-insight** — target: under 90 seconds from upload to AI insight

### Key PM Artifacts
- [Full PRD](pm/PRD.md) — problem, goals, user stories, technical requirements, risks
- [User Research](pm/user_research.md) — 3 personas, JTBD framework, opportunity sizing
- [RICE Prioritisation](pm/prioritisation.md) — 10 features scored and ranked
- [Competitive Analysis](pm/competitive_analysis.md) — vs ChatGPT, Julius AI, Tableau

---

## 🏃 Agile Process

Built across 3 sprints using GitHub Issues as a kanban board.

| Sprint | Theme | Delivered |
|--------|-------|-----------|
| Sprint 1 | Foundation | Upload, profiling, auto charts |
| Sprint 2 | AI Intelligence | Gemini Q&A, insights, custom charts |
| Sprint 3 | Polish + Ship | PDF export, QA tests, CI/CD, deploy |

Full sprint plans, standups, and retrospectives in [`agile/`](agile/)

---

## 🧠 AI/ML Concepts Used

- **Prompt engineering** — structured prompts for consistent JSON output
- **Context window management** — sending compact data summaries, not raw data
- **Output parsing** — robust JSON extraction with fallback handling
- **Grounded generation** — AI answers are grounded in actual dataset statistics

---

## 📊 Sample Dataset

The built-in sample dataset contains 1,000 rows of synthetic electronics sales data:
- 8 products across 2 categories
- 4 regions
- 12 months of daily transactions
- Revenue, quantity, unit price, returns

Use it to demo the app without uploading your own data.

---

## 🔒 Security

- API keys stored in `.streamlit/secrets.toml` never committed to Git
- No raw data sent to AI; only statistical summaries
- No user data stored; everything lives in session state only
- `secrets.toml` explicitly excluded in `.gitignore`

---

## 🗺️ Roadmap

- [ ] User authentication + saved sessions
- [ ] Database connections (Postgres, BigQuery)
- [ ] Scheduled email reports
- [ ] Team collaboration features
- [ ] Fine-tuned model on business analytics

---

## 👩‍💻 Author

**Anusha Singh**
