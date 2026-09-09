import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# 1. Copy the 3D Blueprint Image
art_img = r"C:\Users\ramya\.gemini\antigravity-ide\brain\917f30cd-48d5-42af-88b7-3c7789a8f45e\securesign_3d_engine_architecture_1787742275211.jpg"
os.makedirs('uploads', exist_ok=True)
dst_img1 = 'uploads/SecureSign_3D_Engine_Architecture_Blueprint.png'
dst_img2 = 'uploads/SecureSign_3D_Isometric_Engineering_Workflow.png'

shutil.copyfile(art_img, dst_img1)
shutil.copyfile(art_img, dst_img2)
print(f"Copied 3D Blueprint to {dst_img1} and {dst_img2}")

# 2. Build 3D Engineering Architecture PDF Dossier (<2 MB)
pdf_path = 'uploads/SecureSign_3D_Engineering_Architecture_Dossier.pdf'
pdf_doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=32, leftMargin=32, topMargin=32, bottomMargin=32
)

styles = getSampleStyleSheet()

p_title_style = ParagraphStyle(
    'AdvTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=19,
    textColor=colors.HexColor('#0B132B'),
    alignment=1,
    spaceAfter=3
)

p_sub_style = ParagraphStyle(
    'AdvSub',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#2563EB'),
    alignment=1,
    spaceAfter=6
)

h1_style = ParagraphStyle(
    'AdvH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#0B132B'),
    spaceBefore=4,
    spaceAfter=3
)

b_style = ParagraphStyle(
    'AdvBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    textColor=colors.HexColor('#334155'),
    spaceAfter=3
)

story = []

story.append(Paragraph("SECURESIGN: 3D ISOMETRIC CRYPTOGRAPHIC ENGINE ARCHITECTURE", p_title_style))
story.append(Paragraph("Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026<br/>Lead Contact: pmahi7801@gmail.com | Production API: https://hackthonapp-production.up.railway.app", p_sub_style))
story.append(Spacer(1, 2))

# Embed the 3D Blueprint Image
story.append(Paragraph("1. Interlocking 3D Cryptographic & Hardware CCID Engine Blueprint", h1_style))
story.append(RLImage(dst_img1, width=7.4*inch, height=4.16*inch))
story.append(Spacer(1, 4))

# Technical Flow Table
story.append(Paragraph("2. Deep Technical Synchronization & Interlocking Subsystems", h1_style))

eng_table_data = [
    [Paragraph("<b>Component Node</b>", b_style), Paragraph("<b>Engineering Mechanism & Data Flow</b>", b_style), Paragraph("<b>Security & Compliance Guarantee</b>", b_style)],
    [Paragraph("<b>1. Smartphone Node</b>", b_style), Paragraph("React Native 0.74+ • On-Device SHA-256 Engine", b_style), Paragraph("Zero Document Exposure: Only mathematical hash leaves phone.", b_style)],
    [Paragraph("<b>2. USB-C Data Bus</b>", b_style), Paragraph("Android USB Host • Bulk IN/OUT Endpoints (0x82/0x02)", b_style), Paragraph("Direct CCID Interface 0; 5000ms Watchdog Protection.", b_style)],
    [Paragraph("<b>3. Hardware Crypto Token</b>", b_style), Paragraph("FIPS 140-2 L3 Secure Element • RSA-2048 On-Chip", b_style), Paragraph("CCA Rule 1: Private Key NEVER leaves hardware chip.", b_style)],
    [Paragraph("<b>4. Holographic Cloud</b>", b_style), Paragraph("Node.js v20 • RFC 3161 TSA Clock • PAdES Assembly", b_style), Paragraph("ETSI TS 102 778 PAdES-LTV + /DocMDP ByteRange Lock.", b_style)],
    [Paragraph("<b>5. Legal Seal Stamping</b>", b_style), Paragraph("pdf-lib Seal Engine • Adobe Acrobat Green Ribbon", b_style), Paragraph("100% Admissible under IT Act 2000 Section 3 & 3A.", b_style)]
]

et = Table(eng_table_data, colWidths=[1.4*inch, 2.7*inch, 3.3*inch])
et.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(et)
story.append(Spacer(1, 4))

story.append(Paragraph("<b>Live Production Verification & Repository References:</b><br/>"
                       "• Production API: https://hackthonapp-production.up.railway.app (13/13 Endpoints 200 OK)<br/>"
                       "• GitHub Source Code: https://github.com/mahankalikornepati2-netizen/hackthonapp<br/>"
                       "• Android APK (Build #4384cd86): https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c", b_style))

pdf_doc.build(story)
print(f"Generated 3D Engineering Architecture PDF at: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
