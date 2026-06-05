# Manual Test Cases — InsightPilot AI

## TC-01: Upload valid CSV
**Steps:** Upload sample_sales.csv  
**Expected:** Profile displays, row/column count correct, no errors  
**Status:** ✅ Pass

## TC-02: Upload Excel file
**Steps:** Upload an .xlsx file  
**Expected:** Loads correctly, same profile behaviour as CSV  
**Status:** ✅ Pass

## TC-03: Upload invalid file type
**Steps:** Upload a .pdf or .txt file  
**Expected:** Clear error message, app does not crash  
**Status:** ✅ Pass

## TC-04: Upload empty CSV (headers only, no data)
**Steps:** Upload a CSV with column headers but 0 data rows  
**Expected:** Handles gracefully, shows "0 rows" in profile, no crash  
**Status:** ✅ Pass

## TC-05: Upload CSV with missing values
**Steps:** Upload a CSV with NaN/blank cells  
**Expected:** Missing cell count shown correctly in profile  
**Status:** ✅ Pass

## TC-06: Auto charts generate for numeric-only dataset
**Steps:** Upload a CSV with only numeric columns, no dates or categories  
**Expected:** At minimum histogram and correlation heatmap render  
**Status:** ✅ Pass

## TC-07: Ask AI a valid question
**Steps:** Upload data → navigate to Ask AI → type "what is the total revenue?"  
**Expected:** AI returns a relevant answer with a number  
**Status:** ✅ Pass

## TC-08: Ask AI with no API key
**Steps:** Clear API key from sidebar → ask a question  
**Expected:** Warning message shown, no crash  
**Status:** ✅ Pass

## TC-09: Generate PDF with insights
**Steps:** Generate AI insights → navigate to Report → click Generate PDF  
**Expected:** PDF downloads, contains insights section  
**Status:** ✅ Pass

## TC-10: Generate PDF without insights
**Steps:** Skip Ask AI page → navigate to Report → generate PDF  
**Expected:** PDF generates without insights section, no crash  
**Status:** ✅ Pass

## TC-11: Navigate to page without uploading data
**Steps:** Go directly to Visualise, Ask AI, or Report page without uploading  
**Expected:** Warning message shown on each page, no crash  
**Status:** ✅ Pass

## TC-12: Upload very wide dataset (20+ columns)
**Steps:** Upload a CSV with 25 columns  
**Expected:** Profile shows all columns, PDF caps at 10 columns with note  
**Status:** ✅ Pass