# Sprint 1 — Foundation
**Dates:** Week 1 (Days 1–4)  
**Goal:** User can upload a CSV and see a full data profile + auto-charts

## Sprint Backlog
| Issue | Story | Points | Status |
|-------|-------|--------|--------|
| #1 | CSV upload and file validation | 2 | ✅ Done |
| #2 | Data profiling and column analysis | 3 | ✅ Done |
| #3 | Auto chart generation | 3 | ✅ Done |
| #10 | Excel file support | 1 | ✅ Done |

**Total points committed:** 9  
**Total points delivered:** 9

## Daily Standup Log
**Day 1:** Set up project structure, installed dependencies, created sample data ✅  
**Day 2:** Built data_processor.py: load, clean, profile functions ✅  
**Day 3:** Built chart_builder.py: 5 auto chart types ✅  
**Day 4:** Built Upload page and Visualise page, tested end to end ✅  

## Sprint Review
**Demo:** Upload sample_sales.csv → profile displays correctly → 5 auto-charts render  
**Outcome:** All 4 issues completed. Charts render correctly for numeric + categorical + date columns.

## Sprint Retrospective
**What went well:**
- Utility-first approach (building utils before pages) kept pages clean
- Sample data made testing fast; no need to find a real dataset every time

**What didn't go well:**
- Chart builder initially failed on datasets with no datetime column — edge case missed
- Took longer than expected to figure out Plotly transparent backgrounds

**Action items for Sprint 2:**
- Add defensive checks in chart_builder.py for missing column types ✅ (done inline)
- Time-box debugging sessions to 20 min before searching for help