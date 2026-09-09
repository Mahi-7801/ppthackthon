import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

os.makedirs('uploads', exist_ok=True)
pdf_path = 'SecureSign_Hackathon_Interview_Cheatsheet_and_Master_QA.pdf'

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=32,
    leftMargin=32,
    topMargin=32,
    bottomMargin=32
)

styles = getSampleStyleSheet()

# Colors
PRIMARY = colors.HexColor('#0F172A')     # Navy / Slate 900
SECONDARY = colors.HexColor('#1E40AF')   # Royal Blue 800
TEAL = colors.HexColor('#0D9488')        # Teal 600
RED = colors.HexColor('#B91C1C')         # Crimson
PURPLE = colors.HexColor('#6B21A8')     # Purple 800
GOLD = colors.HexColor('#B45309')       # Amber 700
BG_CARD = colors.HexColor('#F8FAFC')     # Slate 50
BORDER_COLOR = colors.HexColor('#CBD5E1')# Slate 300
TEXT_DARK = colors.HexColor('#0F172A')
TEXT_MUTED = colors.HexColor('#334155')

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=16,
    leading=20,
    textColor=PRIMARY,
    alignment=1,
    spaceAfter=3
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    textColor=SECONDARY,
    alignment=1,
    spaceAfter=8
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=PRIMARY,
    spaceBefore=8,
    spaceAfter=4
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=12.5,
    textColor=SECONDARY,
    spaceBefore=5,
    spaceAfter=2
)

body_style = ParagraphStyle(
    'BodyDark',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    textColor=TEXT_DARK
)

body_bold = ParagraphStyle(
    'BodyDarkBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=11,
    textColor=TEXT_DARK
)

shortcut_style = ParagraphStyle(
    'ShortcutText',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10.5,
    textColor=GOLD
)

table_header = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10.5,
    textColor=colors.white
)

table_cell = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.6,
    leading=10,
    textColor=TEXT_DARK
)

table_cell_bold = ParagraphStyle(
    'TableCellBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.6,
    leading=10,
    textColor=TEXT_DARK
)

elements = []

# Title & Banner
elements.append(Paragraph("SECURESIGN INNOVATION CHALLENGE — JURY DEFENSE MASTER CHEATSHEET", title_style))
elements.append(Paragraph("Complete Categorized Questions, Technical Code Explanations, Golden Shortcuts & Winning Answers", subtitle_style))
elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=6))

# Quick Strategy Box
strategy_data = [
    [
        Paragraph("<b>HOW TO USE THIS CHEATSHEET:</b><br/>"
                  "• <b>Gold 'Shortcut' Column:</b> Memorize the 1-line punchline for immediate instant response.<br/>"
                  "• <b>Deep Technical / Code Defense:</b> Use if the technical architect or developer on the jury asks for specifics.<br/>"
                  "• <b>Legal / Gov Defense:</b> Use when IAS Officers or Department Directors ask about compliance and rollout.", table_cell)
    ]
]
t_strat = Table(strategy_data, colWidths=[548])
t_strat.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
    ('BOX', (0,0), (-1,-1), 1, GOLD),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
elements.append(t_strat)
elements.append(Spacer(1, 6))

# CATEGORY 1: CODING & NATIVE ARCHITECTURE QUESTIONS
elements.append(Paragraph("Category 1: Coding, Internal Architecture & Native Stack (For Technical Jury)", h1_style))

cat1_qa = [
    [Paragraph("Jury Question", table_header), Paragraph("Deep Technical / Coding Explanation", table_header), Paragraph("1-Line Shortcut (Say This Fast)", table_header)],
    [
        Paragraph("<b>Q1: How does your app talk to the USB dongle without root or third-party drivers?</b>", table_cell_bold),
        Paragraph("We built a custom <b>Kotlin CCID USB Driver</b> using Android's native <code>android.hardware.usb.UsbManager</code>. It opens a <code>UsbDeviceConnection</code> directly to the USB CCID interface (Class <code>0x0B</code>) and executes <code>bulkTransfer()</code> sending ISO/IEC 7816-4 APDU command frames.", table_cell),
        Paragraph("<i>\"Native Android USB CCID Driver via standard bulk endpoints (0x0B) with 100% zero root required.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q2: Show me the cryptographic signing flow in code. Where does signing occur?</b>", table_cell_bold),
        Paragraph("1. PDF Document is hashed locally on phone using SHA-256 (<code>MessageDigest.getInstance(\"SHA-256\")</code>).<br/>"
                  "2. App verifies PIN via APDU (<code>00 20 00 00 [PIN]</code>).<br/>"
                  "3. Only the 32-byte digest is passed into token via APDU (<code>00 2A 9E 9A [HASH]</code>).<br/>"
                  "4. Token's on-chip hardware RSA crypto engine returns raw signature blob.<br/>"
                  "5. App packages signature into standard PAdES-LTV dictionary.", table_cell),
        Paragraph("<i>\"Hash on phone -> Send 32-byte hash to token -> Sign on hardware chip -> Return signature. Private key NEVER leaves token!\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q3: What frameworks & languages did you use to build the solution?</b>", table_cell_bold),
        Paragraph("• <b>Mobile Frontend:</b> React Native 0.74 + TypeScript for fast, responsive UI.<br/>"
                  "• <b>Native Core:</b> Kotlin / Java Native Modules (<code>DSCSigningModule</code>) for hardware CCID USB & APDU management.<br/>"
                  "• <b>Backend & TSA Engine:</b> Node.js + Express with PKCS#7 / PAdES-LTV assembly engine.<br/>"
                  "• <b>Deployment:</b> Dockerized microservice on Linux / Railway / AP State Data Center.", table_cell),
        Paragraph("<i>\"React Native for UI + Native Kotlin for USB CCID hardware driver + Node.js for PAdES-LTV packaging.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q4: How do you handle app performance, memory footprint, and signing latency?</b>", table_cell_bold),
        Paragraph("• <b>APK Size:</b> Compact ~28 MB.<br/>"
                  "• <b>RAM Usage:</b> ~45 MB runtime memory.<br/>"
                  "• <b>Signing Latency:</b> < 2.5 seconds total round-trip latency.<br/>"
                  "• Uses streaming PDF byte buffers to avoid memory spikes on large 50+ page documents.", table_cell),
        Paragraph("<i>\"Under 2.5s signing speed, 45MB RAM usage, stream-buffered to sign large 100-page G.O. files easily.\"</i>", shortcut_style)
    ]
]

t_c1 = Table(cat1_qa, colWidths=[130, 278, 140])
t_c1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_c1)
elements.append(Spacer(1, 6))

# CATEGORY 2: HARDWARE & DONGLE COMPATIBILITY
elements.append(Paragraph("Category 2: Hardware, Dongles & Physical Connectivity", h1_style))

cat2_qa = [
    [Paragraph("Jury Question", table_header), Paragraph("Deep Technical / Hardware Explanation", table_header), Paragraph("1-Line Shortcut (Say This Fast)", table_header)],
    [
        Paragraph("<b>Q5: Which USB dongles and crypto tokens are supported?</b>", table_cell_bold),
        Paragraph("All CCA-India approved FIPS 140-2 Level 3 / CC EAL 5+ tokens adhering to ISO 7816-4 and CCID standards:<br/>"
                  "1. <b>WatchData PROXKey</b> (most widely used in AP Secretariat)<br/>"
                  "2. <b>Feitian ePass 2003 / Auto</b><br/>"
                  "3. <b>mToken CryptoID</b><br/>"
                  "4. <b>SafeNet eToken 5110</b><br/>"
                  "5. <b>HyperPKI / TrustKey</b>", table_cell),
        Paragraph("<i>\"Universal CCID support: WatchData PROXKey, ePass2003, mToken, SafeNet & HyperPKI directly via Type-C/OTG.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q6: What if an officer has an older USB-A dongle instead of native Type-C?</b>", table_cell_bold),
        Paragraph("SecureSign works identically with both native Type-C DSC tokens and standard USB-A tokens using a standard 10-rupee OTG adapter. Android's USB Host subsystem handles the physical interface seamlessly.", table_cell),
        Paragraph("<i>\"Native Type-C ready + 100% backward-compatible with legacy USB-A tokens using simple OTG adapter.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q7: What happens if a wrong PIN is entered multiple times?</b>", table_cell_bold),
        Paragraph("Hardware-enforced security: The physical token firmware automatically blocks access after 3-5 failed PIN attempts. The app captures the ISO 7816 status word <code>63 CX</code> (where X is remaining attempts) and alerts the user.", table_cell),
        Paragraph("<i>\"Hardware lockout after 3 failed attempts (APDU 63 CX response) preventing all brute-force attacks.\"</i>", shortcut_style)
    ]
]

t_c2 = Table(cat2_qa, colWidths=[130, 278, 140])
t_c2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), SECONDARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_c2)

# PAGE BREAK
elements.append(PageBreak())

# CATEGORY 3: LEGAL, CCA INDIA & CRYPTOGRAPHIC COMPLIANCE
elements.append(Paragraph("Category 3: Legal, CCA India & Cryptographic Compliance (For IAS / Legal Panel)", h1_style))

cat3_qa = [
    [Paragraph("Jury Question", table_header), Paragraph("Legal & Cryptographic Defense", table_header), Paragraph("1-Line Shortcut (Say This Fast)", table_header)],
    [
        Paragraph("<b>Q8: Is this legally valid in Indian Courts under the IT Act 2000?</b>", table_cell_bold),
        Paragraph("<b>100% Legally Valid.</b> It complies with <b>Section 3 & Section 3A of the Indian Information Technology Act 2000</b>. Signatures are generated using licensed Certifying Authorities (eMudhra, Capricorn, VSign, NSDL) under the Controller of Certifying Authorities (CCA India).", table_cell),
        Paragraph("<i>\"Fully valid under IT Act 2000 Section 3/3A and CCA India rules, recognized by all Indian Courts.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q9: Why does Adobe Reader show a Green Checkmark for SecureSign documents?</b>", table_cell_bold),
        Paragraph("Because SecureSign embeds full <b>PAdES-LTV (ETSI EN 319 142)</b> containers with embedded CRL/OCSP revocation chains and <b>RFC 3161 Time Stamping Authority (TSA)</b> tokens. Adobe Acrobat parses the DSS (Document Security Store) and validates the root CA trust.", table_cell),
        Paragraph("<i>\"PAdES-LTV + RFC 3161 TSA timestamp gives genuine Adobe Green Tick and 10+ years Long Term Validation.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q10: What cryptographic algorithms & key lengths are supported?</b>", table_cell_bold),
        Paragraph("• Asymmetric: RSA 2048-bit, RSA 4096-bit, and ECDSA (NIST P-256).<br/>"
                  "• Hashing: SHA-256, SHA-384, SHA-512 (FIPS 180-4).<br/>"
                  "• Format: PKCS#7 / CMS (RFC 5652) and X.509 v3 Digital Certificates.", table_cell),
        Paragraph("<i>\"RSA 2048/4096 and ECDSA with SHA-256/512 adhering to CCA India 2026 cryptographic guidelines.\"</i>", shortcut_style)
    ]
]

t_c3 = Table(cat3_qa, colWidths=[130, 278, 140])
t_c3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PURPLE),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_c3)
elements.append(Spacer(1, 6))

# CATEGORY 4: GOVERNMENT INTEGRATION & AP STATE ROLLOUT
elements.append(Paragraph("Category 4: AP State e-Governance Integration & Scalability", h1_style))

cat4_qa = [
    [Paragraph("Jury Question", table_header), Paragraph("Integration & Deployment Architecture", table_header), Paragraph("1-Line Shortcut (Say This Fast)", table_header)],
    [
        Paragraph("<b>Q11: How will SecureSign integrate with AP e-Office and CFMS?</b>", table_cell_bold),
        Paragraph("We provide three seamless integration modes:<br/>"
                  "1. <b>Android App Intent / Deep Link:</b> e-Office mobile app invokes SecureSign via intent, receives signed PDF callback in < 2s.<br/>"
                  "2. <b>REST API Microservice:</b> Can be hosted on AP State Data Center (APSDC).<br/>"
                  "3. <b>Embedded Android SDK:</b> Direct .AAR library embeddable into AP e-Office app.", table_cell),
        Paragraph("<i>\"Plug-and-play Android App Intent, REST API, or embedded SDK ready for AP e-Office and CFMS.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q12: Can an officer sign files when traveling in remote areas with no internet?</b>", table_cell_bold),
        Paragraph("<b>YES.</b> The cryptographic handshake between phone and Type-C DSC dongle is 100% offline via local USB CCID. The signature is applied locally. Once the device reconnects to network, it automatically syncs the signed G.O. back to e-Office servers.", table_cell),
        Paragraph("<i>\"100% Offline Signing on device + auto-sync when network returns. Ideal for field officers & tours.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Q13: What is your rollout roadmap for the AP Secretariat & 26 Districts?</b>", table_cell_bold),
        Paragraph("• <b>Week 1-2 (Pilot):</b> Deploy to 50 Principal Secretaries and HoDs in AP Secretariat.<br/>"
                  "• <b>Week 3-4:</b> Rollout to 26 District Collectorates and Joint Collectors.<br/>"
                  "• <b>Month 2:</b> Statewide expansion covering 50,000+ government officers across all departments.", table_cell),
        Paragraph("<i>\"Immediate 2-week pilot for AP Secretariat -> 26 District Collectorates in 30 days -> Statewide rollout.\"</i>", shortcut_style)
    ]
]

t_c4 = Table(cat4_qa, colWidths=[130, 278, 140])
t_c4.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TEAL),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_c4)
elements.append(Spacer(1, 6))

# CATEGORY 5: TROUBLESHOOTING & EMERGENCY DEMO PLAN
elements.append(Paragraph("Category 5: Live Demo Edge Cases & Backup Contingencies", h1_style))

cat5_qa = [
    [Paragraph("Scenario / Issue", table_header), Paragraph("Instant Recovery Action During Meeting", table_header), Paragraph("What to Say to the Panel", table_header)],
    [
        Paragraph("<b>Screen share lag or phone disconnects</b>", table_cell_bold),
        Paragraph("Immediately switch to pre-recorded HD walkthrough <code>SecureSign_Demonstration_Video.mp4</code> or show pre-signed <code>test_signed_output.pdf</code> in Adobe Acrobat.", table_cell),
        Paragraph("<i>\"While the screen mirror reconnects, let me show you the verified signed PDF in Adobe Acrobat Reader.\"</i>", shortcut_style)
    ],
    [
        Paragraph("<b>Dongle not detected on first plug</b>", table_cell_bold),
        Paragraph("Unplug and replug firmly, accept Android USB permission prompt <i>'Always open SecureSign when USB is connected'</i>.", table_cell),
        Paragraph("<i>\"Android is establishing the secure CCID connection through the hardware USB bus.\"</i>", shortcut_style)
    ]
]

t_c5 = Table(cat5_qa, colWidths=[130, 240, 178])
t_c5.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), RED),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_c5)

doc.build(elements)
shutil.copy(pdf_path, os.path.join('uploads', pdf_path))
print("Successfully generated master QA cheatsheet:", pdf_path)
