from fpdf import FPDF
from datetime import datetime
import tempfile
import os


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(79, 129, 189)
        self.cell(0, 10, "InsightPilot AI - Data Analysis Report",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", size=9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 6, f"Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(79, 129, 189)
        self.ln(4)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(79, 129, 189)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def body_text(self, text):
        self.set_font("Helvetica", size=10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(2)


def generate_report(df, profile, insights, filename="report.pdf"):
    report = ReportPDF()
    report.add_page()

    report.section_title("1. Dataset Overview")
    report.body_text(
        f"Rows: {profile['rows']:,}  |  "
        f"Columns: {profile['columns']}  |  "
        f"Missing: {profile['missing_cells']} ({profile['missing_pct']}%)  |  "
        f"Duplicates: {profile['duplicate_rows']}"
    )

    report.section_title("2. Column Summary")
    for col in profile["column_details"]:
        line = (f"- {col['name']} ({col['dtype']}) "
                f"- {col['unique']} unique, {col['nulls']} nulls")
        if "mean" in col:
            line += f" | mean: {col['mean']}, range: [{col['min']} - {col['max']}]"
        report.body_text(line)

    if insights:
        report.section_title("3. AI-Generated Insights")
        for i, ins in enumerate(insights, 1):
            report.set_font("Helvetica", "B", 10)
            report.set_text_color(30, 30, 30)
            report.cell(0, 7,
                        f"{i}. {ins.get('title', '')}  [{ins.get('importance', '')}]",
                        new_x="LMARGIN", new_y="NEXT")
            report.set_font("Helvetica", size=10)
            report.multi_cell(0, 6, ins.get("insight", ""))
            report.set_font("Helvetica", "I", 9)
            report.set_text_color(79, 129, 189)
            report.multi_cell(0, 6, f"-> {ins.get('recommendation', '')}")
            report.set_text_color(30, 30, 30)
            report.ln(2)

    report.section_title("4. Descriptive Statistics")
    stats = df.describe().round(2)
    stats = stats.iloc[:, :10]
    col_width = min(30, 160 // max(len(stats.columns), 1))

    report.set_font("Helvetica", "B", 8)
    report.cell(30, 7, "Stat", border=1)
    for col in stats.columns:
        report.cell(col_width, 7, str(col)[:12], border=1)
    report.ln()

    report.set_font("Helvetica", size=8)
    for idx in stats.index:
        report.cell(30, 6, str(idx), border=1)
        for col in stats.columns:
            report.cell(col_width, 6, str(stats.loc[idx, col]), border=1)
        report.ln()

    output_path = os.path.join(tempfile.gettempdir(), "insightpilot_report.pdf")
    report.output(output_path)
    return output_path