import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

os.makedirs('uploads', exist_ok=True)

img_path = 'uploads/SecureSign_3D_Engine_Architecture_Blueprint.png'
pdf_path = 'uploads/SecureSign_Official_APK_Installation_and_Download_Package.pdf'

pdf_doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=32, leftMargin=32, topMargin=26, bottomMargin=26
)

styles = getSampleStyleSheet()

p_title_style = ParagraphStyle(
    'ApkTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=19,
    textColor=colors.HexColor('#0B132B'),
    alignment=1,
    spaceAfter=3
)

p_sub_style = ParagraphStyle(
    'ApkSub',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#2563EB'),
    alignment=1,
    spaceAfter=6
)

h1_style = ParagraphStyle(
    'ApkH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#0B132B'),
    spaceBefore=4,
    spaceAfter=3
)

b_style = ParagraphStyle(
    'ApkBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    textColor=colors.HexColor('#334155'),
    spaceAfter=2
)

b_bold = ParagraphStyle(
    'ApkBodyBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=11,
    textColor=colors.HexColor('#0B132B')
)

story = []

# ══════════════════════════════════════════════════════════════════════
# PAGE 1: TITLE + DIRECT CLOUD APK DOWNLOAD BANNER + 3D BLUEPRINT
# ══════════════════════════════════════════════════════════════════════
story.append(Paragraph("SECURESIGN: OFFICIAL ANDROID APK PACKAGE & CLOUD INSTALLATION DOSSIER", p_title_style))
story.append(Paragraph("Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026<br/>Lead Contact: pmahi7801@gmail.com | Production API: https://hackthonapp-production.up.railway.app", p_sub_style))
story.append(Spacer(1, 3))

# Direct Cloud Download Callout Box
apk_link_data = [
    [Paragraph("<b>📱 DIRECT STANDALONE APK CLOUD DOWNLOAD (EAS BUILD #4384cd86)</b>", ParagraphStyle('Hdr', parent=b_bold, textColor=colors.white, fontSize=9))],
    [
        Paragraph("<b>Official Verified Cloud URL:</b><br/>"
                  "<font color='#2563EB'><b>https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c</b></font><br/>"
                  "<i>(Note for Evaluators: Because modern native Android APKs with compiled C++ CCID drivers and Hermes engines exceed the Google Form 10 MB direct upload limit, this official verified dossier provides 1-click cloud install access and checksum verification.)</i>", b_style)
    ]
]

alt = Table(apk_link_data, colWidths=[7.36*inch])
alt.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')), # Green Banner
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#10B981')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F0FDF4')]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(alt)
story.append(Spacer(1, 6))

# Embedded 3D Blueprint Graphic
story.append(Paragraph("1. Interlocking 3D Cryptographic & Hardware CCID Engine Blueprint", h1_style))
story.append(Spacer(1, 3))
if os.path.exists(img_path):
    story.append(RLImage(img_path, width=7.36*inch, height=3.6*inch))
story.append(Spacer(1, 6))

# 4 Key Highlights
callout_data = [
    [Paragraph("<b>📱 1. Mobile Client</b>", b_bold), Paragraph("<b>🔌 2. USB-C Data Bus</b>", b_bold), Paragraph("<b>⚡ 3. Hardware Token</b>", b_bold), Paragraph("<b>☁️ 4. Cloud & Legal</b>", b_bold)],
    [
        Paragraph("React Native 0.74+, TypeScript, Expo SDK 51. On-device SHA-256 (32B) digest calculation. Zero document exposure.", b_style),
        Paragraph("Kotlin 1.9+ Android USB Host driver claiming Class 0x0B endpoints (0x82/0x02). RAM zeroized (0x00) immediately.", b_style),
        Paragraph("FIPS 140-2 Level 3 Secure Element. On-chip RSA-2048 signing. Private key NEVER leaves hardware chip (CCA Rule 1).", b_style),
        Paragraph("Node.js v20 LTS, RFC 3161 TSA Clock, pdf-lib visible seal stamping, PAdES-LTV container (IT Act Sec 3A valid).", b_style)
    ]
]

ct = Table(callout_data, colWidths=[1.84*inch, 1.84*inch, 1.84*inch, 1.84*inch])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(ct)

# Page Break for Clean 2-Page Layout
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════
# PAGE 2: APPLICATION SPECS, API KEYS, TESTING CREDENTIALS & INSTRUCTIONS
# ══════════════════════════════════════════════════════════════════════
story.append(Paragraph("2. Application Build Specifications & Production API Endpoints", h1_style))
story.append(Spacer(1, 3))

app_specs_data = [
    [Paragraph("<b>Parameter</b>", b_bold), Paragraph("<b>Production Specification Details</b>", b_bold)],
    [Paragraph("Application Name", b_style), Paragraph("SecureSign Mobile", b_style)],
    [Paragraph("Package Identifier", b_style), Paragraph("com.securesign.app (EAS Standalone APK Build)", b_style)],
    [Paragraph("EAS Build Identifier", b_style), Paragraph("4384cd86-8e73-42f3-ad81-033d7bbb9d2c (Expo Application Services)", b_style)],
    [Paragraph("Target Platform", b_style), Paragraph("Android 8.0 (API Level 26) through Android 15 (API Level 35)", b_style)],
    [Paragraph("Hardware USB Interface", b_style), Paragraph("USB Type-C CCID Host Mode (Bulk IN 0x82 / Bulk OUT 0x02, Class 0x0B)", b_style)],
    [Paragraph("Supported DSC Tokens", b_style), Paragraph("Feitian ePass2003 / Auto, Watchdata ProxKey, Gemalto IDPrime, mToken", b_style)],
    [Paragraph("Production REST API", b_style), Paragraph("https://hackthonapp-production.up.railway.app (TLS 1.3 HTTPS)", b_style)],
    [Paragraph("Evaluator Test Account", b_style), Paragraph("mahankalikornepati@gmail.com", b_style)],
    [Paragraph("Evaluation Certificate Serial", b_style), Paragraph("98A00302010202107F83B1657FF1FC53 (CCA Class-3 Hardware DSC)", b_style)],
    [Paragraph("GitHub Source Code", b_style), Paragraph("https://github.com/mahankalikornepati2-netizen/hackthonapp", b_style)],
    [Paragraph("Statutory Compliance", b_style), Paragraph("100% Indian IT Act 2000 Section 3A & ETSI EN 319 142-1 (PAdES-LTV)", b_style)]
]

ast = Table(app_specs_data, colWidths=[2.2*inch, 5.16*inch])
ast.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(ast)
story.append(Spacer(1, 8))

# Step-by-Step Instructions
story.append(Paragraph("3. Step-by-Step Testing & Verification Instructions for Evaluators", h1_style))
story.append(Spacer(1, 3))

steps_data = [
    [Paragraph("<b>Step #</b>", b_bold), Paragraph("<b>Action / Testing Procedure</b>", b_bold), Paragraph("<b>Expected Output / Result</b>", b_bold)],
    [
        Paragraph("1. Install", b_style),
        Paragraph("Open link on Android device: https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c and tap Install.", b_style),
        Paragraph("SecureSign Mobile icon appears on home screen.", b_style)
    ],
    [
        Paragraph("2. Connect", b_style),
        Paragraph("Plug any standard USB Type-C DSC Token (ePass2003 / ProxKey) into smartphone USB port.", b_style),
        Paragraph("Android prompts USB permission; app detects CCID Class 0x0B.", b_style)
    ],
    [
        Paragraph("3. Select PDF", b_style),
        Paragraph("Tap 'Pick Document to Sign (PDF)' and select any PDF document.", b_style),
        Paragraph("App computes SHA-256 digest on-device with zero plaintext leakage.", b_style)
    ],
    [
        Paragraph("4. Enter PIN", b_style),
        Paragraph("Input 8-digit Token PIN (e.g. 12345678) on secure keypad and tap 'Confirm & Sign'.", b_style),
        Paragraph("ISO 7816-4 VERIFY executed; RAM buffer zeroized (0x00) immediately.", b_style)
    ],
    [
        Paragraph("5. Verify", b_style),
        Paragraph("Tap 'Download & Open Signed PDF' to inspect the output file in Adobe Acrobat Reader.", b_style),
        Paragraph("Adobe Acrobat displays Green Verification Ribbon ('Signature is VALID').", b_style)
    ]
]

stt = Table(steps_data, colWidths=[0.8*inch, 3.8*inch, 2.76*inch])
stt.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(stt)
story.append(Spacer(1, 8))

# Bottom Contact
story.append(Paragraph("<b>Submission Contacts:</b><br/>"
                       "• Registered Lead Innovator: pmahi7801@gmail.com<br/>"
                       "• Evaluator Testing Account: mahankalikornepati@gmail.com<br/>"
                       "• Live API Endpoint: https://hackthonapp-production.up.railway.app", b_style))

pdf_doc.build(story)

# Also copy to alias
shutil.copyfile(pdf_path, 'uploads/SecureSign_APK_Download_and_Installation_Dossier.pdf')

print(f"Generated Official APK Package PDF at: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
