# Sprint 3 — Polish + Ship
**Dates:** Week 2 (Days 9–12)  
**Goal:** PDF export works, QA complete, app deployed

## Sprint Backlog
| Issue | Story | Points | Status |
|-------|-------|--------|--------|
| #6 | PDF report generation | 3 | ✅ Done |
| #11 | Unit tests — data_processor | 2 | ✅ Done |
| #12 | Unit tests — chart_builder | 2 | ✅ Done |
| #13 | Unit tests — ai_analyst | 2 | ✅ Done |
| #14 | Manual test execution | 2 | ✅ Done |
| #7 | Deploy to Streamlit Cloud | 1 | ✅ Done |

**Total points committed:** 12  
**Total points delivered:** 12

## Sprint Retrospective
**What went well:**
- FPDF2 was straightforward once we understood the cell/multi_cell API
- Streamlit Cloud deployment was genuinely one-click

**What didn't go well:**
- PDF broke on datasets with 15+ columns — stats table overflowed page width
- Had to cap stats table at 10 columns and add a note

**Lessons learned:**
- Always test PDF generator with wide datasets, not just the sample one
- Write tests before fixing bugs,caught 2 regressions during unit testing