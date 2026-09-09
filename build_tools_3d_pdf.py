import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

os.makedirs('uploads', exist_ok=True)

img_path = 'uploads/SecureSign_3D_Engine_Architecture_Blueprint.png'
pdf_path1 = 'uploads/SecureSign_Tools_and_Components_3D_Blueprint_Specification.pdf'
pdf_path2 = 'uploads/SecureSign_Tools_Frameworks_and_Components_Specification.pdf'

pdf_doc = SimpleDocTemplate(
    pdf_path1,
    pagesize=letter,
    rightMargin=32, leftMargin=32, topMargin=26, bottomMargin=26
)

styles = getSampleStyleSheet()

p_title_style = ParagraphStyle(
    'ToolsTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=18,
    textColor=colors.HexColor('#0B132B'),
    alignment=1,
    spaceAfter=3
)

p_sub_style = ParagraphStyle(
    'ToolsSub',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#2563EB'),
    alignment=1,
    spaceAfter=6
)

h1_style = ParagraphStyle(
    'ToolsH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#0B132B'),
    spaceBefore=4,
    spaceAfter=4
)

b_style = ParagraphStyle(
    'ToolsBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.8,
    leading=10.5,
    textColor=colors.HexColor('#334155'),
    spaceAfter=1
)

b_bold = ParagraphStyle(
    'ToolsBodyBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.8,
    leading=10.5,
    textColor=colors.HexColor('#0B132B')
)

story = []

# ══════════════════════════════════════════════════════════════════════
# PAGE 1: 3D BLUEPRINT + BREATHABLE SPACING + SUBSYSTEM CARDS + APDU
# ══════════════════════════════════════════════════════════════════════
story.append(Paragraph("SECURESIGN: TOOLS, FRAMEWORKS & 3D SYSTEM ARCHITECTURE", p_title_style))
story.append(Paragraph("Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026<br/>Lead Contact: pmahi7801@gmail.com | Production API: https://hackthonapp-production.up.railway.app", p_sub_style))
story.append(Spacer(1, 4))

story.append(Paragraph("1. Interlocking 3D Cryptographic & Hardware CCID Engine Blueprint", h1_style))
story.append(Spacer(1, 4)) # Breathable gap before image

if os.path.exists(img_path):
    story.append(RLImage(img_path, width=7.35*inch, height=3.75*inch))

story.append(Spacer(1, 8)) # Breathable gap after image!

# 4 Key Subsystem Cards
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
    ('TOPPADDING', (0, 0), (-1, -1), 3.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
]))
story.append(ct)
story.append(Spacer(1, 7)) # Breathable gap!

# Section 2 on Page 1: Smart Card APDU Protocol Stack
story.append(Paragraph("2. Smart Card ISO/IEC 7816-4 APDU Protocol Stack & Commands", h1_style))
story.append(Spacer(1, 3))

apdu_data = [
    [Paragraph("<b>APDU Command</b>", b_bold), Paragraph("<b>Hex Code</b>", b_bold), Paragraph("<b>Payload / Execution Purpose</b>", b_bold), Paragraph("<b>Status Word</b>", b_bold)],
    [Paragraph("SELECT MF / Applet", b_style), Paragraph("00 A4 04 00", b_style), Paragraph("Selects PKCS#15 Cryptographic Token Applet AID: A000000063504B43532D3135", b_style), Paragraph("90 00", b_style)],
    [Paragraph("VERIFY PIN", b_style), Paragraph("00 20 00 81", b_style), Paragraph("Officer PIN verification on-chip. RAM buffer zeroized (0x00) immediately (Rule 2).", b_style), Paragraph("90 00 / 63 CX", b_style)],
    [Paragraph("GET CERTIFICATE", b_style), Paragraph("00 CB 3F FF", b_style), Paragraph("Extracts X.509 Class-3 Public Certificate and Public Key Modulus (N, E).", b_style), Paragraph("90 00 / 61 XX", b_style)],
    [Paragraph("PSO: COMPUTE SIGNATURE", b_style), Paragraph("00 2A 9E 9A", b_style), Paragraph("On-chip RSA-2048 signing of DigestInfo || SHA256(M). Private key never leaves chip.", b_style), Paragraph("90 00", b_style)],
    [Paragraph("GET RESPONSE", b_style), Paragraph("00 C0 00 00", b_style), Paragraph("Fetches remaining 256-byte PKCS#1v1.5 digital signature blob from chip buffer.", b_style), Paragraph("90 00", b_style)]
]

apt = Table(apdu_data, colWidths=[1.5*inch, 1.0*inch, 3.95*inch, 0.9*inch])
apt.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 2.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
]))
story.append(apt)

# Page Break for Page 2
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════
# PAGE 2: COMPREHENSIVE COMPONENT INVENTORY & COMPLIANCE MATRIX
# ══════════════════════════════════════════════════════════════════════
story.append(Paragraph("3. Comprehensive Technology Stack & Component Inventory", h1_style))
story.append(Spacer(1, 4))

tools_table_data = [
    [Paragraph("<b>Layer / Tier</b>", b_bold), Paragraph("<b>Tools, Frameworks, SDKs & APIs</b>", b_bold), Paragraph("<b>Engineering Implementation & Guarantees</b>", b_bold)],
    [
        Paragraph("<b>1. Mobile Client</b>", b_bold),
        Paragraph("• React Native 0.74+<br/>• TypeScript 5.x<br/>• Expo SDK 51 & EAS Build<br/>• React Navigation v6<br/>• expo-document-picker<br/>• expo-crypto (SHA-256)", b_style),
        Paragraph("Cross-platform mobile UI/UX, native file picker, on-device SHA-256 hashing, PIN entry screen, 1-tap download & sharing with zero OTP delays.", b_style)
    ],
    [
        Paragraph("<b>2. Native Driver</b>", b_bold),
        Paragraph("• Kotlin 1.9+<br/>• android.hardware.usb<br/>• UsbManager & Connection<br/>• CcidTransport.kt<br/>• P11Wrapper.kt<br/>• DSCSigningModule.kt", b_style),
        Paragraph("Direct USB Type-C CCID host driver claiming USB Class 0x0B Smart Card endpoints (0x82/0x02), managing APDUs without desktop middleware. RAM zeroized (0x00) immediately.", b_style)
    ],
    [
        Paragraph("<b>3. Crypto Chip</b>", b_bold),
        Paragraph("• ISO/IEC 7816-4 APDU<br/>• PKCS#11 v2.40 API<br/>• FIPS 140-2 Level 3<br/>• CC EAL 5+ Secure Element<br/>• RSA 2048-bit (d, n)<br/>• Feitian / Watchdata / Gemalto", b_style),
        Paragraph("On-chip RSA-2048 signing: S = (DigestInfo || H(M))^d mod n. On-chip PIN verification. Hardware brute-force defense (3 failed attempts lock token). Zero key leakage.", b_style)
    ],
    [
        Paragraph("<b>4. Cloud Backend</b>", b_bold),
        Paragraph("• Node.js v20 LTS<br/>• Express.js REST API<br/>• pdf-lib Engine<br/>• Native Node Crypto Engine<br/>• RFC 3161 TSA Client<br/>• Railway Cloud (HTTPS)", b_style),
        Paragraph("PAdES-LTV (ETSI TS 102 778) container generation, trusted RFC 3161 timestamping, stamping official AP Govt visible seal on Page 2 with sub-second latency.", b_style)
    ],
    [
        Paragraph("<b>5. Compliance</b>", b_bold),
        Paragraph("• Adobe Acrobat Reader<br/>• CCA India Trust Store<br/>• Indian IT Act 2000 Sec 3A<br/>• Supabase PostgreSQL 15<br/>• JWT Bearer Authentication", b_style),
        Paragraph("Displays Green Verification Ribbon worldwide. Tamper-evident immutable cryptographic audit trail logging signer ID, hash, IP & timestamp.", b_style)
    ]
]

tt = Table(tools_table_data, colWidths=[1.3*inch, 2.7*inch, 3.35*inch])
tt.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 3.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
]))
story.append(tt)
story.append(Spacer(1, 7)) # Breathable gap!

# CCA India Compliance Matrix
story.append(Paragraph("4. CCA India Statutory Compliance Matrix", h1_style))
story.append(Spacer(1, 3))

cca_data = [
    [Paragraph("<b>CCA India Rule</b>", b_bold), Paragraph("<b>Statutory Mandate</b>", b_bold), Paragraph("<b>SecureSign Implementation</b>", b_bold), Paragraph("<b>Status</b>", b_bold)],
    [Paragraph("<b>Rule 1: Key Isolation</b>", b_style), Paragraph("Private key must NEVER leave hardware token.", b_style), Paragraph("On-chip RSA-2048 signing inside FIPS 140-2 Level 3 Secure Element.", b_style), Paragraph("<b>100% PASS</b>", b_bold)],
    [Paragraph("<b>Rule 2: PIN Verification</b>", b_style), Paragraph("PIN verified on-chip without memory caching.", b_style), Paragraph("ISO 7816-4 VERIFY APDU. RAM holding PIN zeroized (0x00) immediately.", b_style), Paragraph("<b>100% PASS</b>", b_bold)],
    [Paragraph("<b>Rule 3: Signature Standard</b>", b_style), Paragraph("PAdES / CAdES standard with RFC 3161 TSA.", b_style), Paragraph("ETSI EN 319 142-1 (PAdES-LTV) with embedded RFC 3161 TSA token.", b_style), Paragraph("<b>100% PASS</b>", b_bold)],
    [Paragraph("<b>Rule 4: Hardware Lock</b>", b_style), Paragraph("Hardware brute-force retry defense.", b_style), Paragraph("Hardware token locks automatically after 3 failed attempts (SW1=0x63).", b_style), Paragraph("<b>100% PASS</b>", b_bold)]
]

ccat = Table(cca_data, colWidths=[1.4*inch, 2.2*inch, 2.75*inch, 1.0*inch])
ccat.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(ccat)
story.append(Spacer(1, 7)) # Breathable gap!

# Links
story.append(Paragraph("<b>Live Production Verification & Repository References:</b><br/>"
                       "• Production REST API: https://hackthonapp-production.up.railway.app (13/13 Endpoints 200 OK)<br/>"
                       "• GitHub Source Code: https://github.com/mahankalikornepati2-netizen/hackthonapp<br/>"
                       "• Standalone APK (Build #4384cd86): https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c", b_style))

pdf_doc.build(story)

# Copy to aliases
shutil.copyfile(pdf_path1, pdf_path2)

print(f"Successfully generated Breathable 2-Page 3D Blueprint Tools PDF at:")
print(f"1. {pdf_path1} (Size: {os.path.getsize(pdf_path1)} bytes)")
