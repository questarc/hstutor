import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def parse_flashcards(raw_text: str):
    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    cards = []
    for line in lines:
        if "Term:" in line or "Question:" in line:
            parts = line.split("–")
            front = parts[0].strip()
            back = parts[1].strip() if len(parts) > 1 else ""
            cards.append({"Front": front, "Back": back})
    return cards

def flashcards_to_csv_bytes(raw_text: str):
    cards = parse_flashcards(raw_text)
    df = pd.DataFrame(cards)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

def flashcards_to_pdf_bytes(raw_text: str, title="Flashcards"):
    cards = parse_flashcards(raw_text)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)
    y -= 40
    c.setFont("Helvetica", 12)
    for card in cards:
        text = f"{card['Front']}  |  {card['Back']}"
        if y < 80:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)
        c.drawString(50, y, text)
        y -= 20
    c.save()
    buf.seek(0)
    return buf.getvalue()
