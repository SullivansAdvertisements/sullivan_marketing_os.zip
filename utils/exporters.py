from pathlib import Path
from datetime import datetime
import pandas as pd
from fpdf import FPDF

EXPORT_DIR = Path("exports")
SAVE_DIR = Path("saved_plans")
EXPORT_DIR.mkdir(exist_ok=True)
SAVE_DIR.mkdir(exist_ok=True)

def export_csv(df: pd.DataFrame, filename: str) -> str:
    path = EXPORT_DIR / filename
    df.to_csv(path, index=False)
    return str(path)

def save_plan_text(text: str, filename: str | None = None) -> str:
    filename = filename or f"campaign_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = SAVE_DIR / filename
    path.write_text(text, encoding="utf-8")
    return str(path)

def export_pdf(title: str, body: str, filename: str) -> str:
    path = EXPORT_DIR / filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    safe = body.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 6, safe)
    pdf.output(str(path))
    return str(path)
