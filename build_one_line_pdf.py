import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

os.makedirs('uploads', exist_ok=True)
pdf_path = 'SecureSign_One_Line_Pocket_Cheatsheet.pdf'

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=28,
    leftMargin=28,
    topMargin=24,
    bottomMargin=24
)

styles = getSampleStyleSheet()

# Colors
PRIMARY = colors.HexColor('#0F172A')
SECONDARY = colors.HexColor('#1E40AF')
GOLD = colors.HexColor('#92400E')
BG_LIGHT = colors.HexColor('#F8FAFC')
BORDER_COLOR = colors.HexColor('#CBD5E1')

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=17,
    textColor=PRIMARY,
    alignment=1,
    spaceAfter=2
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    textColor=SECONDARY,
    alignment=1,
    spaceAfter=6
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=11,
    textColor=PRIMARY,
    spaceBefore=4,
    spaceAfter=2
)

table_header = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.white
)

table_cell_q = ParagraphStyle(
    'TableCellQ',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.2,
    leading=9.2,
    textColor=PRIMARY
)

table_cell_ans = ParagraphStyle(
    'TableCellAns',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.2,
    leading=9.2,
    textColor=colors.HexColor('#1E3A8A')
)

elements = []

elements.append(Paragraph("SECURESIGN — ULTRA SIMPLE 1-LINE POCKET CHEATSHEET", title_style))
elements.append(Paragraph("Tomorrow's Meeting (08-09-2026 @ 11:30 AM): Meet Link -> https://meet.google.com/cmz-hrzn-bvr", subtitle_style))
elements.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=4))

# 1-Line Q&A Table
qa_rows = [
    [Paragraph("Topic / Question Asked by Panel", table_header), Paragraph("Exact 1-Line Answer to Say (Memorize This)", table_header)],
    
    # Core Demo & Pitch
    [
        Paragraph("<b>1. What is SecureSign in 1 line?</b>", table_cell_q),
        Paragraph("<b>\"Mobile digital signing app that lets officers sign PDFs directly using USB Type-C DSC dongles without a PC.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>2. How does mobile talk to dongle?</b>", table_cell_q),
        Paragraph("<b>\"Native Android USB CCID Driver (Class 0x0B) communicating directly via ISO 7816 APDU commands without root.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>3. Does private key leave the dongle?</b>", table_cell_q),
        Paragraph("<b>\"Never. The key stays locked in the crypto chip; only the 32-byte SHA-256 document hash is signed on-hardware.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>4. What is your tech stack?</b>", table_cell_q),
        Paragraph("<b>\"React Native for UI + Native Kotlin for USB CCID hardware driver + Node.js for PAdES-LTV packaging.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>5. Which dongle brands work?</b>", table_cell_q),
        Paragraph("<b>\"All CCA tokens: WatchData PROXKey, ePass2003, mToken, and SafeNet directly via Type-C or OTG.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>6. Is it legally valid in India?</b>", table_cell_q),
        Paragraph("<b>\"100% legally valid under Section 3 & 3A of the IT Act 2000 and CCA India guidelines.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>7. Why does Adobe show Green Tick?</b>", table_cell_q),
        Paragraph("<b>\"Because it creates PAdES-LTV (ETSI EN 319 142) signatures with embedded RFC 3161 TSA timestamps.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>8. How fast is it & memory size?</b>", table_cell_q),
        Paragraph("<b>\"Signs in under 2.5 seconds, takes only 45MB RAM, and handles 100-page G.O. documents easily.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>9. What if wrong PIN is entered?</b>", table_cell_q),
        Paragraph("<b>\"Hardware automatically locks after 3 failed attempts, completely preventing brute-force attacks.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>10. Does it work without Internet?</b>", table_cell_q),
        Paragraph("<b>\"Yes, cryptographic signing is 100% offline on the phone, and auto-syncs when internet reconnects.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>11. How to integrate with AP e-Office?</b>", table_cell_q),
        Paragraph("<b>\"Through plug-and-play Android App Intent, REST API, or our pre-built Android SDK (.AAR).\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>12. What is your rollout plan?</b>", table_cell_q),
        Paragraph("<b>\"Immediate 2-week pilot for AP Secretariat, expanding to 26 District Collectorates in 30 days.\"</b>", table_cell_ans)
    ],
    [
        Paragraph("<b>13. If screen share lags during demo?</b>", table_cell_q),
        Paragraph("<b>\"Immediately play backup video (SecureSign_Demonstration_Video.mp4) or show test_signed_output.pdf in Adobe.\"</b>", table_cell_ans)
    ]
]

t_table = Table(qa_rows, colWidths=[175, 373])
t_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
    ('TOPPADDING', (0,0), (-1,-1), 2.8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_table)
elements.append(Spacer(1, 4))

# 4-Step Demo Formula
elements.append(Paragraph("<b>4-STEP LIVE DEMO FORMULA (30 SECONDS WALKTHROUGH):</b>", h1_style))
demo_formula = [
    [
        Paragraph("<b>1. PLUG</b><br/>Plug Type-C Dongle into Phone", table_cell_q),
        Paragraph("<b>2. DETECT</b><br/>App shows Token & Certificate", table_cell_q),
        Paragraph("<b>3. PIN & SIGN</b><br/>Enter PIN -> Signs in 2 seconds", table_cell_q),
        Paragraph("<b>4. VERIFY</b><br/>Open in Adobe -> Green Checkmark Valid", table_cell_q)
    ]
]
t_demo = Table(demo_formula, colWidths=[137, 137, 137, 137])
t_demo.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
    ('BOX', (0,0), (-1,-1), 1, GOLD),
    ('GRID', (0,0), (-1,-1), 0.5, GOLD),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
elements.append(t_demo)

doc.build(elements)
shutil.copy(pdf_path, os.path.join('uploads', pdf_path))
print("Successfully generated 1-line pocket cheatsheet:", pdf_path)
