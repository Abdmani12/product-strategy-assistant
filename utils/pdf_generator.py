import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable


class PDFReportGenerator:
    """Generates a professional executive PDF report from agent analysis results."""

    BRAND_BLUE = colors.HexColor("#1B3A6B")
    BRAND_ACCENT = colors.HexColor("#2E86AB")
    BRAND_LIGHT = colors.HexColor("#EBF4FA")
    BRAND_GREEN = colors.HexColor("#28A745")
    BRAND_ORANGE = colors.HexColor("#FD7E14")
    TEXT_DARK = colors.HexColor("#212529")
    TEXT_GRAY = colors.HexColor("#6C757D")
    DIVIDER = colors.HexColor("#DEE2E6")

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._build_custom_styles()

    def _build_custom_styles(self):
        self.h_cover = ParagraphStyle(
            "CoverTitle", parent=self.styles["Title"],
            fontSize=28, textColor=colors.white,
            spaceAfter=12, alignment=TA_CENTER, leading=34
        )
        self.h_cover_sub = ParagraphStyle(
            "CoverSub", parent=self.styles["Normal"],
            fontSize=14, textColor=colors.HexColor("#B0C4DE"),
            alignment=TA_CENTER, spaceAfter=6
        )
        self.h1 = ParagraphStyle(
            "H1", parent=self.styles["Heading1"],
            fontSize=18, textColor=self.BRAND_BLUE,
            spaceBefore=18, spaceAfter=8, leading=22
        )
        self.h2 = ParagraphStyle(
            "H2", parent=self.styles["Heading2"],
            fontSize=14, textColor=self.BRAND_ACCENT,
            spaceBefore=12, spaceAfter=6, leading=18
        )
        self.h3 = ParagraphStyle(
            "H3", parent=self.styles["Heading3"],
            fontSize=12, textColor=self.TEXT_DARK,
            spaceBefore=8, spaceAfter=4, leading=16, fontName="Helvetica-Bold"
        )
        self.body = ParagraphStyle(
            "Body", parent=self.styles["Normal"],
            fontSize=10, textColor=self.TEXT_DARK,
            leading=15, spaceAfter=6, alignment=TA_JUSTIFY
        )
        self.bullet = ParagraphStyle(
            "Bullet", parent=self.styles["Normal"],
            fontSize=10, textColor=self.TEXT_DARK,
            leading=14, spaceAfter=3, leftIndent=20, bulletIndent=8
        )
        self.caption = ParagraphStyle(
            "Caption", parent=self.styles["Normal"],
            fontSize=8, textColor=self.TEXT_GRAY,
            alignment=TA_CENTER, spaceAfter=4
        )

    def generate(self, analysis_results: dict, uploaded_file_names: list) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            leftMargin=2.2 * cm, rightMargin=2.2 * cm,
            topMargin=2 * cm, bottomMargin=2 * cm,
            title="Product Strategy Executive Report",
            author="AI Product Strategy Assistant"
        )
        story = []
        story += self._cover_page(uploaded_file_names)
        story += self._toc_section(analysis_results)
        story += self._sections(analysis_results)
        story += self._appendix(uploaded_file_names)
        doc.build(story, onFirstPage=self._first_page_header, onLaterPages=self._later_pages_header)
        return buffer.getvalue()

    def _cover_page(self, file_names: list):
        elements = []
        # Blue cover background via a table
        cover_content = [
            [Paragraph("AI-Powered Product Strategy", self.h_cover)],
            [Paragraph("Executive Intelligence Report", self.h_cover)],
            [Spacer(1, 0.3 * inch)],
            [Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.h_cover_sub)],
            [Paragraph("Powered by Multi-Agent AI Analysis", self.h_cover_sub)],
        ]
        cover_table = Table(cover_content, colWidths=[17 * cm])
        cover_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.BRAND_BLUE),
            ("TOPPADDING", (0, 0), (-1, -1), 18),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
            ("LEFTPADDING", (0, 0), (-1, -1), 24),
            ("RIGHTPADDING", (0, 0), (-1, -1), 24),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [self.BRAND_BLUE]),
        ]))
        elements.append(Spacer(1, 1.5 * inch))
        elements.append(cover_table)
        elements.append(Spacer(1, 0.5 * inch))

        # Data sources box
        if file_names:
            source_data = [["Data Sources Analyzed"]]
            for f in file_names:
                source_data.append([f"• {f}"])
            src_table = Table(source_data, colWidths=[17 * cm])
            src_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), self.BRAND_ACCENT),
                ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
                ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (0, 0), 11),
                ("BACKGROUND", (0, 1), (-1, -1), self.BRAND_LIGHT),
                ("TEXTCOLOR", (0, 1), (-1, -1), self.TEXT_DARK),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("BOX", (0, 0), (-1, -1), 1, self.BRAND_ACCENT),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, self.DIVIDER),
            ]))
            elements.append(src_table)

        elements.append(PageBreak())
        return elements

    def _toc_section(self, results: dict):
        elements = [Paragraph("Table of Contents", self.h1), HRFlowable(width="100%", color=self.BRAND_ACCENT, thickness=1.5)]
        sections = [
            ("1", "Customer Feedback Analysis", "customer_feedback"),
            ("2", "Market Research Summary", "market_research"),
            ("3", "Competitor Analysis", "competitor_analysis"),
            ("4", "SWOT Analysis", "swot_analysis"),
            ("5", "Feature Prioritization", "feature_prioritization"),
            ("6", "Strategic Recommendations", "strategy_recommendations"),
            ("7", "Executive Summary", "executive_summary"),
        ]
        toc_data = [["#", "Section", "Status"]]
        for num, title, key in sections:
            status = "✓ Completed" if key in results and results[key] else "— Not Available"
            status_color = self.BRAND_GREEN if key in results and results[key] else self.TEXT_GRAY
            toc_data.append([num, title, status])

        toc_table = Table(toc_data, colWidths=[1 * cm, 13 * cm, 4 * cm])
        toc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), self.BRAND_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, self.BRAND_LIGHT]),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("BOX", (0, 0), (-1, -1), 1, self.BRAND_ACCENT),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, self.DIVIDER),
            ("TEXTCOLOR", (2, 1), (2, -1), self.BRAND_GREEN),
        ]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(toc_table)
        elements.append(PageBreak())
        return elements

    def _sections(self, results: dict):
        section_map = [
            ("customer_feedback", "1. Customer Feedback Analysis", "Customer Insights Report"),
            ("market_research", "2. Market Research Summary", "Market Intelligence"),
            ("competitor_analysis", "3. Competitor Analysis", "Competitive Landscape"),
            ("swot_analysis", "4. SWOT Analysis", "Strategic Position Assessment"),
            ("feature_prioritization", "5. Feature Prioritization", "Product Development Priorities"),
            ("strategy_recommendations", "6. Strategic Recommendations & Roadmap", "Strategic Action Plan"),
            ("executive_summary", "7. Executive Summary", "Board-Level Overview"),
        ]
        elements = []
        for key, section_title, subtitle in section_map:
            if key in results and results[key]:
                elements += self._render_section(section_title, subtitle, results[key])
                elements.append(PageBreak())
        return elements

    def _render_section(self, title: str, subtitle: str, content: str):
        elements = []
        # Section header bar
        header_data = [[Paragraph(title, ParagraphStyle("SecH", parent=self.h1, textColor=colors.white, spaceBefore=0, spaceAfter=0))]]
        header_table = Table(header_data, colWidths=[17 * cm])
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.BRAND_BLUE),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ]))
        elements.append(header_table)
        elements.append(Paragraph(subtitle, ParagraphStyle("SubT", parent=self.caption, fontSize=10, textColor=self.BRAND_ACCENT, spaceAfter=10, spaceBefore=4)))
        elements.append(HRFlowable(width="100%", color=self.DIVIDER, thickness=0.5))
        elements.append(Spacer(1, 0.1 * inch))

        # Parse and render content
        for para in self._parse_markdown(content):
            elements.append(para)
            elements.append(Spacer(1, 0.04 * inch))

        return elements

    def _parse_markdown(self, text: str):
        """Convert markdown-like text to ReportLab paragraphs."""
        paragraphs = []
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            if not line:
                i += 1
                continue
            if line.startswith("### "):
                paragraphs.append(Paragraph(self._clean(line[4:]), self.h3))
            elif line.startswith("## "):
                paragraphs.append(Paragraph(self._clean(line[3:]), self.h2))
            elif line.startswith("# "):
                paragraphs.append(Paragraph(self._clean(line[2:]), self.h2))
            elif line.startswith(("- ", "* ", "• ")):
                paragraphs.append(Paragraph(f"• {self._clean(line[2:])}", self.bullet))
            elif line.startswith(("  - ", "  * ")):
                paragraphs.append(Paragraph(f"  – {self._clean(line[4:])}", ParagraphStyle("BulletSub", parent=self.bullet, leftIndent=36, fontSize=9)))
            elif line and line[0].isdigit() and ". " in line[:4]:
                paragraphs.append(Paragraph(self._clean(line), self.bullet))
            elif line.startswith("**") and line.endswith("**") and len(line) > 4:
                paragraphs.append(Paragraph(f"<b>{self._clean(line[2:-2])}</b>", self.body))
            elif line.startswith("---") or line.startswith("==="):
                paragraphs.append(HRFlowable(width="100%", color=self.DIVIDER, thickness=0.5))
            else:
                paragraphs.append(Paragraph(self._clean(line), self.body))
            i += 1
        return paragraphs

    def _clean(self, text: str) -> str:
        """Escape special XML characters and handle basic markdown bold/italic."""
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Bold: **text**
        import re
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
        # Italic: *text*
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        return text

    def _appendix(self, file_names: list):
        elements = [Paragraph("Appendix: Data Sources", self.h1), HRFlowable(width="100%", color=self.BRAND_ACCENT, thickness=1.5)]
        elements.append(Spacer(1, 0.15 * inch))
        elements.append(Paragraph("The following data sources were analyzed to generate this report:", self.body))
        for f in file_names:
            elements.append(Paragraph(f"• {f}", self.bullet))
        elements.append(Spacer(1, 0.2 * inch))
        disclaimer = (
            "This report was generated by an AI-powered multi-agent system. All insights and recommendations "
            "are based on the data provided and are intended to support, not replace, human decision-making. "
            "Validate key findings with additional sources before making major strategic decisions."
        )
        disclaimer_data = [[Paragraph(f"<i>{disclaimer}</i>", ParagraphStyle("Disc", parent=self.body, fontSize=9, textColor=self.TEXT_GRAY, alignment=TA_JUSTIFY))]]
        disc_table = Table(disclaimer_data, colWidths=[17 * cm])
        disc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.BRAND_LIGHT),
            ("BOX", (0, 0), (-1, -1), 1, self.BRAND_ACCENT),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        elements.append(disc_table)
        return elements

    def _first_page_header(self, canvas, doc):
        pass  # Cover page has no header/footer

    def _later_pages_header(self, canvas, doc):
        canvas.saveState()
        page_width = A4[0]
        # Header line
        canvas.setStrokeColor(self.BRAND_ACCENT)
        canvas.setLineWidth(1)
        canvas.line(2.2 * cm, A4[1] - 1.5 * cm, page_width - 2.2 * cm, A4[1] - 1.5 * cm)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(self.BRAND_BLUE)
        canvas.drawString(2.2 * cm, A4[1] - 1.3 * cm, "AI Product Strategy Report — CONFIDENTIAL")
        canvas.drawRightString(page_width - 2.2 * cm, A4[1] - 1.3 * cm, datetime.now().strftime("%B %Y"))
        # Footer line
        canvas.setStrokeColor(self.DIVIDER)
        canvas.line(2.2 * cm, 1.5 * cm, page_width - 2.2 * cm, 1.5 * cm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(self.TEXT_GRAY)
        canvas.drawString(2.2 * cm, 1.1 * cm, "Powered by Multi-Agent AI Analysis")
        canvas.drawRightString(page_width - 2.2 * cm, 1.1 * cm, f"Page {doc.page}")
        canvas.restoreState()
