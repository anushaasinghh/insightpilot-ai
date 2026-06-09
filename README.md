# 🧠 InsightPilot AI

![CI](https://github.com/anushaasinghh/insightpilot-ai/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![Features](https://img.shields.io/badge/Features-11-purple)

> **Upload any CSV or Excel file and get AI-powered business insights,
> anomaly detection, correlation analysis, executive summaries, and a
> downloadable PDF report — in under 90 seconds.**
> No data team. No SQL. No setup.

## 🔗 [Live App](https://insightpilot-ai-data-analysis.streamlit.app/) · [PM Documentation](pm/) · [Sprint History](agile/) · [Test Suite](qa/)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📁 **Upload & Profile** | CSV or Excel. Auto-cleans column names, detects types, shows missing %, duplicates, memory |
| 🏆 **Data Quality Score** | 0–100 score with grade (A–F), issue breakdown, and actionable recommendations |
| 📊 **Auto Charts** | 5 chart types generated automatically — time series, bar, distribution, pie, heatmap |
| 🔴 **Anomaly Detection** | Z-score based detection with adjustable sensitivity — flags outliers on interactive charts |
| 🔗 **Correlation Insights** | Plain-English explanations of relationships between columns — no statistics degree needed |
| 🛠️ **Custom Chart Builder** | Pick any columns, any chart type, any colour grouping |
| ⬇️ **PNG Chart Download** | Download any chart as a high-resolution PNG with one click |
| 🤖 **AI Insights** | One click → 5 ranked business insights powered by Google Gemini |
| 📋 **Executive Summary** | 4-sentence AI briefing: what the data covers, top finding, top risk, recommended action |
| 💬 **Persistent Q&A Chat** | Ask plain English questions — chat history saved across page refreshes via SQLite |
| ⚖️ **Comparative Analysis** | Upload 2 CSVs — instantly see what changed, which metrics moved, side-by-side charts |
| 📄 **PDF Report** | Download a complete report with profile, stats, and AI insights |

---

## 🗂️ Full Project Lifecycle

This project was built following a complete product development lifecycle —
not just the engineering side.

| Layer | What's included | Location |
|-------|----------------|----------|
| **Product Management** | PRD, user research, personas, competitive analysis, RICE prioritisation | [`pm/`](pm/) |
| **Agile** | 3 sprint plans, daily standups, retrospectives, definition of done | [`agile/`](agile/) |
| **Engineering** | Python, Streamlit, Gemini API, Plotly, FPDF2, SQLite | [`utils/`](utils/), [`pages/`](pages/) |
| **QA** | 29 unit tests, test plan, 12 manual test cases | [`qa/`](qa/) |
| **CI/CD** | GitHub Actions — auto-runs tests on every push | [`.github/workflows/`](.github/workflows/) |
| **Deployment** | Streamlit Cloud — free, live public URL | [Live App](https://insightpilot-ai-data-analysis.streamlit.app/) |

---

## 🏗️ Project Structure

```
insightpilot-ai/
├── app.py                        # Main landing page
├── pages/
│   ├── 1_upload.py               # Upload + data profiling + quality score
│   ├── 2_visualise.py            # Auto charts + anomaly detection + correlation insights + PNG download
│   ├── 3_ask_ai.py               # Executive summary + AI insights + persistent Q&A chat
│   ├── 4_report.py               # PDF export
│   └── 5_compare.py              # Comparative analysis — upload 2 CSVs
├── utils/
│   ├── data_processor.py         # Load, clean, profile, quality score, anomaly detection, comparison
│   ├── chart_builder.py          # Plotly charts, anomaly chart, PNG export, correlation plain English
│   ├── ai_analyst.py             # Gemini API — insights, Q&A, executive summary
│   ├── pdf_generator.py          # PDF report generation
│   └── chat_history.py           # SQLite persistent chat storage
├── database/
│   └── insightpilot.db           # Auto-created SQLite database (gitignored)
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
| AI | Google Gemini 2.0 Flash | Insights, Q&A, Executive Summary |
| Data | Pandas, NumPy, SciPy | Processing, analysis, anomaly detection |
| Charts | Plotly + Kaleido | Interactive visualisations + PNG export |
| PDF | FPDF2 | Report generation |
| Database | SQLite | Persistent chat history |
| Testing | pytest | Unit tests |
| CI/CD | GitHub Actions | Automated test pipeline |
| Deployment | Streamlit Cloud | Free hosting |

---

## 🔴 Anomaly Detection — How It Works

InsightPilot uses the **Z-score method** to detect anomalies:

```
Z = (value - mean) / standard_deviation
```

Any value with |Z| > 3.0 is flagged — this occurs in only 0.3% of normally distributed data.
The threshold is adjustable (1.5–5.0) so you can tune sensitivity for your dataset.
Anomalies are highlighted in red on interactive charts with upper/lower threshold lines shown.

---

## 🏆 Data Quality Score — How It's Calculated

| Penalty | Condition | Max Deduction |
|---------|-----------|---------------|
| Missing data | Proportional to % missing | -30 points |
| Duplicate rows | Proportional to % duplicates | -20 points |
| Low-cardinality numeric columns | Numeric columns with < 5 unique values | -3 per column |
| High-cardinality categorical columns | All-unique categorical columns (ID columns) | -3 per column |

Grades: **A (90–100) · B (75–89) · C (60–74) · D (40–59) · F (0–39)**

---

## ⚖️ Comparative Analysis — Use Cases

- **Month vs Month** — upload Jan sales and Feb sales, see what changed
- **Region vs Region** — compare two market segments side by side
- **Before vs After** — measure the impact of a campaign or product change
- **No matching columns?** — the tool automatically identifies common columns and skips mismatches

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
- **Z-score anomaly detection** — statistical outlier identification
- **Pearson correlation** — relationship strength between numeric variables

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

- API keys stored in `.streamlit/secrets.toml` — never committed to Git
- No raw data sent to AI — only statistical summaries
- Chat history stored locally in SQLite — never sent to any server
- `secrets.toml` and `database/` explicitly excluded in `.gitignore`

---

## 🗺️ Roadmap

- [x] Data Quality Score
- [x] Anomaly Detection
- [x] Correlation Plain English Insights
- [x] Executive Summary
- [x] Persistent Chat History
- [x] Comparative Analysis (2 CSVs)
- [x] PNG Chart Download
- [ ] User authentication + saved sessions
- [ ] Database connections (Postgres, BigQuery)
- [ ] Scheduled email reports
- [ ] Team collaboration features
- [ ] Fine-tuned model on business analytics

---

## 👩‍💻 Author

**Anusha Singh**
