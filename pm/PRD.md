# Product Requirements Document — InsightPilot AI
**Version:** 1.0  
**Status:** Approved  
**Author:** [Your Name]  
**Last Updated:** June 2026

## 1. Problem Statement
Non-technical business users (marketers, ops analysts, founders) have access to data but lack the tools, time, or skills to extract insights from it quickly. Existing tools are either too complex (Tableau), too generic (ChatGPT), or too expensive (enterprise BI).

## 2. Proposed Solution
A web app where users upload any CSV and instantly receive:
auto-generated charts, AI-written insights, natural language Q&A, and a downloadable PDF report, all in under 2 minutes.

## 3. Goals & Success Metrics

### North Star
**Time-to-first-insight** (target: <90 seconds from upload to AI insight)

## Success Metrics

| Goal | Metric | Target | Timeline |
|------|---------|---------|----------|
| Deliver instant value | Time to First Insight | < 90 seconds | Launch |
| Ensure platform reliability | PDF Report Generation Success Rate | > 98% | Launch |
| Build trust in AI outputs | AI Answer Accuracy (User-Rated) | > 80% positive feedback | 30 Days Post-Launch |
| Drive user engagement | 7-Day Retention | > 40% | 60 Days Post-Launch |

### Guardrail Metrics
- AI hallucination rate: <3%
- App load time: <2 seconds
- Error rate on file upload: <1%

## 4. User Stories

### Must Have (P0)
- As a user, I want to upload a CSV and see a data profile instantly
- As a user, I want auto-generated charts without configuring anything
- As a user, I want to ask plain English questions about my data
- As a user, I want to download a PDF report of my analysis

### Should Have (P1)
- As a user, I want a custom chart builder to explore my own questions
- As a user, I want my chat history preserved during my session
- As a user, I want to see AI confidence in its answers

### Won't Have v1.0 (P2)
- User accounts and saved sessions
- Database connections (only file upload)
- Scheduled reports
- Team collaboration


### In Scope (MVP — v1.0)
- Data Quality Score with A–F grading and recommendations
- Anomaly detection using Z-score with interactive visualisation
- Correlation insights in plain English
- Executive Summary generation (4-sentence AI briefing)
- Persistent chat history via SQLite
- Comparative analysis for 2 CSV datasets
- PNG export for all charts
  
## 5. Technical Requirements
- File upload: CSV + Excel, max 50MB
- AI response time: <5 seconds per question
- PDF generation: <10 seconds
- Supported browsers: Chrome, Firefox, Safari (latest 2 versions)
- Mobile: responsive but not optimised (desktop-first)

## 6. Risks
| Risk | Mitigation |
|------|-----------|
| AI gives wrong numbers | Show data summary used; add thumbs up/down |
| Large files cause timeout | Cap at 50MB; show row count warning above 100k |
| API key exposed | Never log keys; use Streamlit secrets in prod |
| PDF layout breaks on edge cases | Unit test PDF generator with 10 dataset types |

## 7. Launch Plan
- Sprint 1: Core upload + charts (Week 1–2)
- Sprint 2: AI Q&A + insights (Week 2–3)  
- Sprint 3: PDF export + polish (Week 3–4)
- Launch: Deploy to Streamlit Cloud, publish to GitHub
