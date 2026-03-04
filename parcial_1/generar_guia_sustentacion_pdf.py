#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / "GUIA_SUSTENTACION_PARCIAL1.pdf"


def main() -> None:
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=1.7 * cm,
        rightMargin=1.7 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.4 * cm,
        title="Guia Sustentacion Parcial 1",
        author="Juan Camilo Ballesteros Sierra",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleX",
        parent=styles["Title"],
        fontSize=18,
        textColor=colors.HexColor("#0b2e59"),
        spaceAfter=10,
    )
    h = ParagraphStyle(
        "HX",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=colors.HexColor("#0b2e59"),
        spaceBefore=6,
        spaceAfter=6,
    )
    p = ParagraphStyle("PX", parent=styles["Normal"], fontSize=10, leading=13)
    mono = ParagraphStyle(
        "Mono",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#202020"),
    )

    story = []
    story.append(Paragraph("Guia Rapida de Sustentacion - Parcial 1", title))
    story.append(Paragraph("Estudiante: Juan Camilo Ballesteros Sierra", p))
    story.append(Paragraph("Codigo: 2230721", p))
    story.append(Paragraph("Profesor: Oscar Hernan Mondragon Martinez", p))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("1) Ventanas recomendadas", h))
    story.append(Paragraph("CMD 1 Host: carpeta de vagrant.", p))
    story.append(Paragraph("CMD 2 Servidor: `vagrant ssh servidor`.", p))
    story.append(Paragraph("CMD 3 Cliente: `vagrant ssh cliente`.", p))
    story.append(Paragraph("Comando inicial:", p))
    story.append(Paragraph("vagrant status", mono))

    story.append(Paragraph("2) Punto 1 DNS", h))
    story.append(Paragraph("Comandos en cliente:", p))
    story.append(Paragraph("dig @192.168.50.2 maestro.empresa.local +short", mono))
    story.append(Paragraph("dig @192.168.50.2 -x 192.168.50.3 +short", mono))
    story.append(Paragraph("dig @192.168.50.2 api2.empresa.local +short", mono))
    story.append(Paragraph("Seguridad:", p))
    story.append(Paragraph("dig @192.168.50.3 empresa.local AXFR +time=2 +tries=1", mono))
    story.append(Paragraph("dig @192.168.50.2 google.com +short", mono))

    story.append(Paragraph("3) Punto 2 Apache + gzip", h))
    story.append(Paragraph("dig @192.168.50.2 parcial.juan-camilo.com +short", mono))
    story.append(
        Paragraph(
            "curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H \"Accept-Encoding: gzip\" -I "
            "http://parcial.juan-camilo.com/lorem.txt",
            mono,
        )
    )
    story.append(
        Paragraph(
            "curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H \"Accept-Encoding: gzip\" -I "
            "http://parcial.juan-camilo.com/logo.png",
            mono,
        )
    )

    story.append(Paragraph("4) Punto 3 ngrok", h))
    story.append(Paragraph("En servidor:", p))
    story.append(Paragraph("bash /tmp/start_point3_ngrok_tunnel.sh", mono))
    story.append(Paragraph("bash /tmp/verify_point3.sh", mono))

    story.append(Paragraph("5) Evidencia lista", h))
    story.append(Paragraph("PDF principal: parcial_1/Evidencias_Parcial1_Juan_Camilo.pdf", p))
    story.append(Paragraph("Capturas: parcial_1/5_evidencia_visual/", p))
    story.append(Paragraph("Repo: github.com/ballesterossmartsolutionssas/servicios-telematicos", p))

    story.append(Paragraph("6) Si preguntan conceptos", h))
    story.append(Paragraph("Recursion off: evita open resolver y abuso DDoS.", p))
    story.append(Paragraph("AXFR restringido: evita exponer toda la zona.", p))
    story.append(Paragraph("gzip: baja bytes de texto y mejora carga.", p))
    story.append(Paragraph("imagenes/video sin gzip: ya vienen comprimidos.", p))

    doc.build(story)
    print(f"PDF generado: {OUT_PDF}")


if __name__ == "__main__":
    main()

