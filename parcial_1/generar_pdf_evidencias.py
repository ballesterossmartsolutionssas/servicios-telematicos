#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import re
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parent
PDF_OUT = ROOT / "Evidencias_Parcial1_Juan_Camilo.pdf"

FILE_P1 = ROOT / "1_punto_dns" / "evidencia_punto1.txt"
FILE_P2 = ROOT / "2_punto_apache_compresion" / "evidencia_punto2_final.txt"
FILE_P3 = ROOT / "3_punto_ngrok" / "evidencia_punto3_final.txt"
FILE_URL = ROOT / "3_punto_ngrok" / "url_publica.txt"

IMG_DIR = ROOT / "5_evidencia_visual"
IMAGES = [
    (IMG_DIR / "01_home_network.png", "Figura 1. Vista de sitio y panel Network."),
    (IMG_DIR / "02_lorem_gzip.png", "Figura 2. lorem.txt con Content-Encoding: gzip."),
    (IMG_DIR / "03_logo_no_gzip.png", "Figura 3. logo.png sin Content-Encoding: gzip."),
]

WIRESHARK_IMAGES = [
    (
        IMG_DIR / "04_wireshark_lorem_gzip.png",
        "Figura 4. Wireshark: respuesta HTTP 200 de lorem.txt con Content-Encoding: gzip.",
    ),
    (
        IMG_DIR / "05_wireshark_logo_200_no_gzip.png",
        "Figura 5. Wireshark: respuesta HTTP 200 de logo.png sin Content-Encoding.",
    ),
]


ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def read_clean_text(path: Path) -> str:
    if not path.exists():
        return f"[No existe archivo: {path}]"
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = ANSI_RE.sub("", raw)
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    cleaned_lines = []
    for line in raw.split("\n"):
        wrapped = textwrap.wrap(line, width=120) or [""]
        cleaned_lines.extend(wrapped)
    return "\n".join(cleaned_lines).strip()


def add_section_title(story, text: str, style):
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(text, style))
    story.append(Spacer(1, 0.15 * cm))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#444444")))
    story.append(Spacer(1, 0.2 * cm))


def add_image_fit(story, img_path: Path, caption: str, max_width: float, max_height: float, style):
    if not img_path.exists():
        story.append(Paragraph(f"Imagen no encontrada: {img_path.name}", style))
        story.append(Spacer(1, 0.15 * cm))
        return

    reader = ImageReader(str(img_path))
    w, h = reader.getSize()
    scale = min(max_width / w, max_height / h)
    draw_w, draw_h = w * scale, h * scale
    story.append(Image(str(img_path), width=draw_w, height=draw_h))
    story.append(Spacer(1, 0.1 * cm))
    story.append(Paragraph(caption, style))
    story.append(Spacer(1, 0.25 * cm))


def main():
    doc = SimpleDocTemplate(
        str(PDF_OUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.4 * cm,
        title="Evidencias Parcial 1 - Juan Camilo Ballesteros Sierra",
        author="Juan Camilo Ballesteros Sierra",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0b2e59"),
        spaceAfter=10,
    )
    h_style = ParagraphStyle(
        "HCustom",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0b2e59"),
    )
    normal = ParagraphStyle("NormalCustom", parent=styles["Normal"], fontSize=10, leading=13)
    code = ParagraphStyle("CodeCustom", parent=styles["Code"], fontSize=7.5, leading=9.2)

    url_text = read_clean_text(FILE_URL)
    p1_text = read_clean_text(FILE_P1)
    p2_text = read_clean_text(FILE_P2)
    p3_text = read_clean_text(FILE_P3)

    story = []
    story.append(Paragraph("EVIDENCIAS PARCIAL 1 - SERVICIOS TELEMATICOS", title_style))
    story.append(Paragraph("Estudiante: Juan Camilo Ballesteros Sierra", normal))
    story.append(Paragraph("Codigo: 2230721", normal))
    story.append(Paragraph("Profesor: Oscar Hernan Mondragon Martinez", normal))
    story.append(Paragraph("Dominio configurado: parcial.juan-camilo.com", normal))
    story.append(Paragraph(f"Fecha de generacion: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal))
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph("URL publica de ngrok:", normal))
    story.append(Preformatted(url_text, code))

    add_section_title(story, "Punto 1 - DNS Maestro/Esclavo", h_style)
    story.append(Preformatted(p1_text, code))
    story.append(PageBreak())

    add_section_title(story, "Punto 2 - Apache + Compresion", h_style)
    story.append(Preformatted(p2_text, code))
    story.append(Spacer(1, 0.2 * cm))
    add_section_title(story, "Evidencia Visual Punto 2", h_style)
    for img_path, caption in IMAGES:
        add_image_fit(
            story,
            img_path,
            caption,
            max_width=doc.width,
            max_height=doc.height * 0.42,
            style=normal,
        )

    add_section_title(story, "Evidencia Wireshark Punto 2", h_style)
    for img_path, caption in WIRESHARK_IMAGES:
        add_image_fit(
            story,
            img_path,
            caption,
            max_width=doc.width,
            max_height=doc.height * 0.42,
            style=normal,
        )

    story.append(PageBreak())
    add_section_title(story, "Punto 3 - Ngrok", h_style)
    story.append(Preformatted(p3_text, code))

    doc.build(story)
    print(f"PDF generado: {PDF_OUT}")


if __name__ == "__main__":
    main()
