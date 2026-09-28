import os
from datetime import datetime
from fpdf import FPDF

EXPORT_FOLDER = "static/exports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)

class ComicPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(79, 70, 229)
        self.cell(0, 10, 'ComicCraft - AI Generated Comic', ln=True, align='C')
        self.ln(5)

def save_pdf(layout: list) -> str:
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", ln=True, align="L")
        pdf.ln(2)

        # Image placement
        image_path = panel['image_path']
        if os.path.exists(image_path):
            pdf.image(image_path, x=15, y=35, w=180, h=110)
            pdf.set_y(155)
        else:
            pdf.set_y(40)
            pdf.set_font('Helvetica', 'I', 11)
            pdf.cell(0, 10, "[Image Not Found]", ln=True)

        # Scene text
        pdf.set_font('Helvetica', 'I', 10)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(0, 6, f"Scene: {panel['scene_description']}")
        pdf.ln(3)

        # Story & Dialogues
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(15, 23, 42)
        pdf.multi_cell(0, 7, panel['text'])

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)
    return pdf_path