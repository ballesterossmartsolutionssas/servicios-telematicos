#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "GUIA_CONTINGENCIA_SUSTENTACION.md"
OUT = ROOT / "GUIA_CONTINGENCIA_SUSTENTACION.pdf"


def main() -> None:
    text = SRC.read_text(encoding="utf-8", errors="replace")

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.3 * cm,
        title="Guia de Contingencia Sustentacion",
        author="Juan Camilo Ballesteros Sierra",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleC",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0b2e59"),
        spaceAfter=8,
    )
    h = ParagraphStyle(
        "HC",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0b2e59"),
        spaceBefore=5,
        spaceAfter=4,
    )
    p = ParagraphStyle("PC", parent=styles["Normal"], fontSize=9.4, leading=12)
    code = ParagraphStyle(
        "CodeC",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8.2,
        leading=10.2,
        textColor=colors.HexColor("#1f1f1f"),
    )

    story = []
    in_code = False
    code_lines: list[str] = []

    def wrap_code_block(lines: list[str], width: int = 72) -> str:
        wrapped_lines: list[str] = []
        for line in lines:
            if not line:
                wrapped_lines.append("")
                continue

            indent_len = len(line) - len(line.lstrip(" "))
            indent = " " * indent_len
            content = line[indent_len:]

            chunks = textwrap.wrap(
                content,
                width=max(20, width - indent_len),
                break_long_words=False,
                break_on_hyphens=False,
                replace_whitespace=False,
                drop_whitespace=False,
            )

            if not chunks:
                wrapped_lines.append(indent)
            else:
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        wrapped_lines.append(f"{indent}{chunk}")
                    else:
                        wrapped_lines.append(f"{indent}  {chunk}")
        return "\n".join(wrapped_lines)

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            story.append(Preformatted(wrap_code_block(code_lines), code))
            story.append(Spacer(1, 0.12 * cm))
            code_lines = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            story.append(Spacer(1, 0.08 * cm))
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:].strip(), title))
            continue
        if line.startswith("## "):
            story.append(Paragraph(line[3:].strip(), h))
            continue

        # markdown-ish list handling
        line = line.replace("`", "")
        if line.startswith("- "):
            line = f"* {line[2:]}"
        if line[:2].isdigit() and line[2:4] == ") ":
            line = line

        story.append(Paragraph(line, p))

    flush_code()
    doc.build(story)
    print(f"PDF generado: {OUT}")


if __name__ == "__main__":
    main()
