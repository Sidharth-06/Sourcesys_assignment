from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, Preformatted, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "ASSIGNMENT_REPORT.md"
OUTPUT = ROOT / "ASSIGNMENT_REPORT.pdf"


def build_styles() -> StyleSheet1:
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#15304a"),
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#1f4e79"),
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubHeading",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#365f91"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextJustified",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#222222"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletText",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            leftIndent=18,
            firstLineIndent=0,
            textColor=colors.HexColor("#222222"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            leftIndent=14,
            rightIndent=14,
            borderPadding=8,
            borderWidth=0.5,
            borderColor=colors.HexColor("#c7d4e3"),
            backColor=colors.HexColor("#f5f8fc"),
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    return styles


def format_inline(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", escaped)
    return escaped


def add_paragraph(story: list, buffer: list[str], style: ParagraphStyle) -> None:
    if not buffer:
        return
    text = " ".join(part.strip() for part in buffer if part.strip())
    if text:
        story.append(Paragraph(format_inline(text), style))
    buffer.clear()


def parse_markdown(text: str, styles: StyleSheet1) -> list:
    story = [Spacer(1, 0.35 * inch)]
    paragraph_buffer: list[str] = []
    code_buffer: list[str] = []
    in_code_block = False
    title_used = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            if in_code_block:
                story.append(Preformatted("\n".join(code_buffer), styles["CodeBlock"]))
                code_buffer.clear()
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        if not stripped:
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            story.append(Spacer(1, 0.08 * inch))
            continue

        if stripped == "---":
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=1,
                    color=colors.HexColor("#b9c7d8"),
                    spaceBefore=8,
                    spaceAfter=10,
                )
            )
            continue

        if stripped.startswith("# "):
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            style_name = "ReportTitle" if not title_used else "SectionHeading"
            title_used = True
            story.append(Paragraph(format_inline(stripped[2:]), styles[style_name]))
            continue

        if stripped.startswith("## "):
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            story.append(Paragraph(format_inline(stripped[3:]), styles["SectionHeading"]))
            continue

        if stripped.startswith("### "):
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            story.append(Paragraph(format_inline(stripped[4:]), styles["SubHeading"]))
            continue

        if stripped.startswith("#### "):
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            story.append(Paragraph(format_inline(stripped[5:]), styles["SubHeading"]))
            continue

        if stripped.startswith("- "):
            add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
            story.append(
                Paragraph(
                    format_inline(stripped[2:]),
                    styles["BulletText"],
                    bulletText="-",
                )
            )
            continue

        paragraph_buffer.append(stripped)

    add_paragraph(story, paragraph_buffer, styles["BodyTextJustified"])
    if code_buffer:
        story.append(Preformatted("\n".join(code_buffer), styles["CodeBlock"]))
    return story


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#4b5b6b"))
    canvas.drawRightString(A4[0] - doc.rightMargin, 20, f"Page {doc.page}")
    canvas.restoreState()


def main() -> None:
    styles = build_styles()
    text = SOURCE.read_text(encoding="utf-8")

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        topMargin=0.75 * inch,
        bottomMargin=0.65 * inch,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
        title="Database Management System Assignment Report",
        author="Codex",
    )
    story = parse_markdown(text, styles)
    document.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    main()
