# Test Plan — InsightPilot AI

## Scope
All four core user flows:
1. Upload + Profile
2. Visualise
3. Ask AI
4. Export PDF

## Test Types
| Type | Tool | When |
|------|------|------|
| Unit tests | pytest | Every commit (via GitHub Actions CI) |
| Manual tests | Test cases doc | End of each sprint |
| Edge case tests | pytest + manual | Before deployment |

## Entry Criteria (start testing when...)
- Feature branch merged to main
- No syntax errors (app runs without crashing)

## Exit Criteria (testing complete when...)
- All unit tests pass
- All manual test cases marked Pass
- Zero P0 bugs open

## Bug Severity Levels
- **P0 — Blocker:** App crashes, data loss, wrong numbers shown to user
- **P1 — Major:** Feature doesn't work but workaround exists
- **P2 — Minor:** UI issue, cosmetic, non-critical