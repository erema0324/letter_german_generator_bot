# -*- coding: utf-8 -*-
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from docx import Document
from docx.shared import Pt


def export_to_pdf(letter_data):
    styles = getSampleStyleSheet()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    story = []

    # Создайте стиль абзаца с отступом
    letter_style = ParagraphStyle(
        name="Letter",
        parent=styles["BodyText"],
        fontSize=12,
        leading=14,
        spaceBefore=0,
        spaceAfter=0,
        alignment=TA_LEFT,
    )

    if "content" in letter_data:
        # Разделите содержимое письма на строки и добавьте абзацы
        content_lines = letter_data["content"].split('\n')
        for line in content_lines:
            content = Paragraph(line, letter_style)
            story.append(content)
            story.append(Spacer(1, 2))

    doc.build(story)
    buffer.seek(0)
    return buffer


def export_to_word(letter_data):
    doc = Document()

    if "content" in letter_data:
        doc.add_paragraph(letter_data["content"])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

