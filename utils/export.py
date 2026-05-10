from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def text_to_txt_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def text_to_pdf_bytes(title: str, body: str) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 54
    c.setFont("Helvetica-Bold", 15)
    c.drawString(54, y, title[:70])
    y -= 28
    c.setFont("Helvetica", 10)
    for paragraph in body.splitlines():
        words = paragraph.split()
        line = ""
        if not words:
            y -= 12
            continue
        for word in words:
            test = f"{line} {word}".strip()
            if len(test) > 95:
                c.drawString(54, y, line)
                y -= 14
                line = word
            else:
                line = test
        if line:
            c.drawString(54, y, line)
            y -= 14
        if y < 54:
            c.showPage()
            y = height - 54
            c.setFont("Helvetica", 10)
    c.save()
    buffer.seek(0)
    return buffer.read()