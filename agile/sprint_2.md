# Sprint 2 — AI Intelligence
**Dates:** Week 1–2 (Days 5–8)  
**Goal:** User can ask AI questions and get auto-generated insights

## Sprint Backlog
| Issue | Story | Points | Status |
|-------|-------|--------|--------|
| #4 | Claude API integration for Q&A | 3 | ✅ Done |
| #5 | AI auto-insights (5 insights JSON) | 3 | ✅ Done |
| #9 | Chat history persistence | 2 | ✅ Done |
| #8 | Custom chart builder | 2 | ✅ Done |

**Total points committed:** 10  
**Total points delivered:** 10

## Sprint Retrospective
**What went well:**
- Gemini API JSON output was reliable with explicit format instructions
- Chat history using st.session_state was simpler than expected

**What didn't go well:**
- First prompt attempt returned markdown fences around JSON, had to add stripping logic
- Custom chart builder had an axis mismatch bug when same column selected for X and Y

**Action items for Sprint 3:**
- Add validation in custom chart: X and Y cannot be the same column
- Add fallback message if AI returns unparseable JSON