import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Nirmala UI for crisp English + Telugu Unicode font rendering
pdfmetrics.registerFont(TTFont('NirmalaUI', 'C:/Windows/Fonts/Nirmala.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('NirmalaUI-Bold', 'C:/Windows/Fonts/Nirmala.ttc', subfontIndex=1))

os.makedirs('uploads', exist_ok=True)
pdf_path = 'SecureSign_Complete_Jury_QA_and_Visual_Workflow_Timeline.pdf'

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=26,
    leftMargin=26,
    topMargin=22,
    bottomMargin=22
)

styles = getSampleStyleSheet()

# Colors
PRIMARY = colors.HexColor('#0F172A')     # Navy Slate 900
SECONDARY = colors.HexColor('#1E40AF')   # Royal Blue 800
TEAL = colors.HexColor('#0D9488')        # Teal 600
RED = colors.HexColor('#B91C1C')         # Crimson 700
PURPLE = colors.HexColor('#6B21A8')     # Purple 800
GOLD = colors.HexColor('#B45309')       # Amber 700
TELUGU_HEADER = colors.HexColor('#065F46')# Emerald 800
BG_CARD = colors.HexColor('#F8FAFC')     # Slate 50
BG_TELUGU = colors.HexColor('#F0FDF4')   # Emerald 50
BORDER_COLOR = colors.HexColor('#CBD5E1')# Slate 300
TEXT_DARK = colors.HexColor('#0F172A')

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='NirmalaUI-Bold',
    fontSize=13,
    leading=16,
    textColor=PRIMARY,
    alignment=1,
    spaceAfter=2
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='NirmalaUI-Bold',
    fontSize=8.5,
    leading=11.5,
    textColor=SECONDARY,
    alignment=1,
    spaceAfter=4
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='NirmalaUI-Bold',
    fontSize=9.5,
    leading=12.5,
    textColor=PRIMARY,
    spaceBefore=5,
    spaceAfter=2
)

table_header = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='NirmalaUI-Bold',
    fontSize=7.2,
    leading=9.2,
    textColor=colors.white
)

table_cell_q = ParagraphStyle(
    'TableCellQ',
    parent=styles['Normal'],
    fontName='NirmalaUI-Bold',
    fontSize=7,
    leading=9,
    textColor=PRIMARY
)

table_cell_eng = ParagraphStyle(
    'TableCellEng',
    parent=styles['Normal'],
    fontName='NirmalaUI',
    fontSize=6.7,
    leading=8.7,
    textColor=TEXT_DARK
)

table_cell_tel = ParagraphStyle(
    'TableCellTel',
    parent=styles['Normal'],
    fontName='NirmalaUI',
    fontSize=6.7,
    leading=8.7,
    textColor=TELUGU_HEADER
)

table_cell_sc_eng = ParagraphStyle(
    'TableCellSCEng',
    parent=styles['Normal'],
    fontName='NirmalaUI-Bold',
    fontSize=6.7,
    leading=8.7,
    textColor=SECONDARY
)

table_cell_sc_tel = ParagraphStyle(
    'TableCellSCTel',
    parent=styles['Normal'],
    fontName='NirmalaUI-Bold',
    fontSize=6.7,
    leading=8.7,
    textColor=GOLD
)

elements = []

# Header & Title
elements.append(Paragraph("SECURESIGN INNOVATION CHALLENGE — JURY DEFENSE & WORKFLOW MASTER", title_style))
elements.append(Paragraph("సెక్యూర్‌సైన్ — పూర్తి టెక్నికల్ సమాధానాలు, డెమో వర్క్‌ఫ్లో & షార్ట్‌కట్ గైడ్ (English & Telugu)", subtitle_style))
elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=3))

# Meeting Details Box (Bilingual)
meeting_box = [
    [
        Paragraph("<b>Meeting Date / మీటింగ్ తేదీ:</b> 08-09-2026 (Tomorrow / రేపు)<br/>"
                  "<b>Time / సమయం:</b> 11:30 AM – 12:30 PM IST (1 Hour / 1 గంట)<br/>"
                  "<b>Google Meet / లింక్:</b> <u>https://meet.google.com/cmz-hrzn-bvr</u>", table_cell_q),
        Paragraph("<b>Organizers / నిర్వాహకులు:</b> Startup AP | AP Innovation Society (ITE&C Dept)<br/>"
                  "<b>Officer / నోడల్ అధికారి:</b> Madan Mohan Mohapatra (Mob: +91-9778627236)<br/>"
                  "<b>Action / చేయవలసినది:</b> Live Mobile Signing Demo + Executive Q&A", table_cell_q)
    ]
]
t_mb = Table(meeting_box, colWidths=[275, 275])
t_mb.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
    ('BOX', (0,0), (-1,-1), 1, GOLD),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
elements.append(t_mb)
elements.append(Spacer(1, 3))

# EMBED WORKFLOW DIAGRAM IMAGE
workflow_img_path = 'uploads/SecureSign_Executive_Workflow_Diagram.png'
if not os.path.exists(workflow_img_path) and os.path.exists('SecureSign_Executive_Workflow_Diagram.png'):
    workflow_img_path = 'SecureSign_Executive_Workflow_Diagram.png'

if os.path.exists(workflow_img_path):
    elements.append(Paragraph("<b>End-to-End Visual Workflow Timeline / ఎండ్-టు-ఎండ్ ఆర్కిటెక్చర్ వర్క్‌ఫ్లో:</b>", h1_style))
    img = RLImage(workflow_img_path, width=550, height=195)
    elements.append(img)
    elements.append(Spacer(1, 3))

# TIMELINE 5-STAGE TABLE (BILINGUAL)
tl_data = [
    [Paragraph("Stage / దశ", table_header), Paragraph("English Technical Flow", table_header), Paragraph("తెలుగు వివరణ (Telugu Flow)", table_header), Paragraph("Time", table_header)],
    [
        Paragraph("<b>Stage 1: Document Ingestion</b><br/>(డాక్యుమెంట్ ఎంపిక)", table_cell_q),
        Paragraph("Officer opens G.O. PDF on Mobile; App generates SHA-256 hash locally.", table_cell_eng),
        Paragraph("అధికారి PDF ఫైల్ ఎంచుకోగానే యాప్ SHA-256 డాక్యుమెంట్ హాష్ తయారు చేస్తుంది.", table_cell_tel),
        Paragraph("<b>< 100ms</b>", table_cell_q)
    ],
    [
        Paragraph("<b>Stage 2: USB CCID Handshake</b><br/>(డోంగిల్ అనుసంధానం)", table_cell_q),
        Paragraph("Kotlin native layer exchanges ATR via USB Class 0x0B and reads X.509 cert.", table_cell_eng),
        Paragraph("మొబైల్ నేరుగా USB CCID డ్రైవర్ ద్వారా డోంగిల్‌ను గుర్తించి సర్టిఫికెట్ రీడ్ చేస్తుంది.", table_cell_tel),
        Paragraph("<b>< 350ms</b>", table_cell_q)
    ],
    [
        Paragraph("<b>Stage 3: On-Chip Crypto Sign</b><br/>(హార్డ్‌వేర్ సంతకం)", table_cell_q),
        Paragraph("User enters PIN; APDU passes 32-byte digest into hardware chip for RSA signing.", table_cell_eng),
        Paragraph("పిన్ కొట్టగానే ప్రైవేట్ కీ బయటకు రాకుండా చిప్ లోపలే సంతకం పూర్తవుతుంది.", table_cell_tel),
        Paragraph("<b>< 800ms</b>", table_cell_q)
    ],
    [
        Paragraph("<b>Stage 4: PAdES-LTV Packaging</b><br/>(టైమ్‌స్టాంప్ భద్రత)", table_cell_q),
        Paragraph("Signature embedded with RFC 3161 TSA Timestamp token & DSS revocation data.", table_cell_eng),
        Paragraph("సంతకానికి RFC 3161 టైమ్‌స్టాంప్ జోడించి 20+ ఏళ్ల చెల్లుబాటు కల్పిస్తుంది.", table_cell_tel),
        Paragraph("<b>< 450ms</b>", table_cell_q)
    ],
    [
        Paragraph("<b>Stage 5: Adobe Verification</b><br/>(గ్రీన్ టిక్ ధృవీకరణ)", table_cell_q),
        Paragraph("Signed G.O. opened in Adobe Reader; Green Tick shows 'Signature is Valid'.", table_cell_eng),
        Paragraph("అడోబ్ రీడర్‌లో తెరవగానే ఆకుపచ్చ టిక్ మార్క్ తో చట్టబద్ధమైన సంతకం కనిపిస్తుంది.", table_cell_tel),
        Paragraph("<b>Instant</b>", table_cell_q)
    ]
]
t_tl = Table(tl_data, colWidths=[105, 185, 200, 60])
t_tl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
elements.append(t_tl)

# PAGE BREAK TO START BILINGUAL Q&A
elements.append(PageBreak())

# SECTION 1: CODING & NATIVE ARCHITECTURE (BILINGUAL)
elements.append(Paragraph("1. Coding, Internal Architecture & Native Drivers (కోడింగ్ & ఆర్కిటెక్చర్)", h1_style))

qa_c1 = [
    [Paragraph("Question (ప్రశ్న)", table_header), Paragraph("English Technical Answer", table_header), Paragraph("తెలుగు సమాధానం (Telugu Answer)", table_header), Paragraph("⚡ 1-Line Shortcut (రెండు భాషలలో)", table_header)],
    [
        Paragraph("<b>Q1: How does mobile talk to dongle without root?</b><br/>(రూట్ లేకుండా మొబైల్ డోంగిల్‌తో ఎలా మాట్లాడుతుంది?)", table_cell_q),
        Paragraph("Custom Kotlin CCID driver uses standard <code>android.hardware.usb.UsbManager</code>. It accesses CCID Class <code>0x0B</code> and sends APDU commands over bulk endpoints.", table_cell_eng),
        Paragraph("ఆండ్రాయిడ్ స్థానిక USB CCID డ్రైవర్ ద్వారా ఎలాంటి రూట్ లేదా థర్డ్-పార్టీ యాప్స్ అవసరం లేకుండా నేరుగా USB బల్క్ ఎండ్‌పాయింట్లతో మాట్లాడుతుంది.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"Native Kotlin USB CCID (0x0B) with zero root.\"</i><br/><b>TE:</b> <i>\"రూట్ లేకుండా నేటివ్ CCID డ్రైవర్ తో పనిచేస్తుంది.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q2: Does Private Key ever leave the dongle?</b><br/>(ప్రైవేట్ కీ డోంగిల్ దాటి బయటకు వస్తుందా?)", table_cell_q),
        Paragraph("<b>NEVER.</b> Key stays in FIPS 140-2 / CC EAL 5+ chip. App only passes 32-byte SHA-256 hash (<code>00 2A 9E 9A</code>) and gets back RSA signature.", table_cell_eng),
        Paragraph("<b>ఎప్పటికీ రాదు.</b> ప్రైవేట్ కీ హార్డ్‌వేర్ చిప్‌లోనే లాక్ అయి ఉంటుంది. కేవలం 32-బైట్ల హాష్ మాత్రమే చిప్‌లోకి వెళ్లి సంతకం పూర్తవుతుంది.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"Private key NEVER leaves token; only hash is signed.\"</i><br/><b>TE:</b> <i>\"ప్రైవేట్ కీ బయటకు రాదు; కేవలం హాష్ మాత్రమే సైన్ అవుతుంది.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q3: What is the Tech Stack?</b><br/>(టెక్నాలజీ స్టాక్ ఏమిటి?)", table_cell_q),
        Paragraph("• UI: React Native 0.74 + TypeScript<br/>• Core: Kotlin Native USB Module<br/>• Backend: Node.js + Express PAdES-LTV", table_cell_eng),
        Paragraph("• యూజర్ ఇంటర్‌ఫేస్: రియాక్ట్ నేటివ్ + టైప్‌స్క్రిప్ట్<br/>• హార్డ్‌వేర్ కోర్: నేటివ్ కోట్లిన్ USB మాడ్యూల్<br/>• బ్యాకెండ్: నోడ్.జేఎస్ PAdES ఇంజిన్", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"React Native + Kotlin CCID + Node.js PAdES.\"</i><br/><b>TE:</b> <i>\"రియాక్ట్ నేటివ్ + కోట్లిన్ డ్రైవర్ + నోడ్.జేఎస్.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q4: How do you sign 100-page G.O. files without lag?</b><br/>(100 పేజీల ఫైళ్లను ఎలా సైన్ చేస్తారు?)", table_cell_q),
        Paragraph("Uses 64KB chunked stream hashing. RAM usage stays under 45MB and signs in < 2.5 seconds.", table_cell_eng),
        Paragraph("64KB స్ట్రీమింగ్ హాషింగ్ వల్ల ఫోన్ మెమరీ 45MB కి మించదు; 100 పేజీల ఫైల్ కూడా 2.5 సెకన్లలో పూర్తవుతుంది.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"64KB chunked stream hashing in <45MB RAM.\"</i><br/><b>TE:</b> <i>\"స్ట్రీమింగ్ వల్ల 45MB ర్యామ్‌తో వేగంగా సైన్ అవుతుంది.\"</i>", table_cell_sc_tel)
    ]
]
t_qc1 = Table(qa_c1, colWidths=[105, 145, 150, 150])
t_qc1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
elements.append(t_qc1)
elements.append(Spacer(1, 3))

# SECTION 2: HARDWARE & DONGLE COMPATIBILITY (BILINGUAL)
elements.append(Paragraph("2. Hardware, Dongles & Power Management (హార్డ్‌వేర్ & డోంగిల్స్)", h1_style))

qa_c2 = [
    [Paragraph("Question (ప్రశ్న)", table_header), Paragraph("English Technical Answer", table_header), Paragraph("తెలుగు సమాధానం (Telugu Answer)", table_header), Paragraph("⚡ 1-Line Shortcut (రెండు భాషలలో)", table_header)],
    [
        Paragraph("<b>Q5: Which dongles are supported?</b><br/>(ఏయే డోంగిల్స్ పనిచేస్తాయి?)", table_cell_q),
        Paragraph("Supports WatchData PROXKey, Feitian ePass2003, mToken CryptoID, SafeNet eToken directly via Type-C/OTG.", table_cell_eng),
        Paragraph("ఆంధ్రా సచివాలయంలో వాడే వాచ్‌డేటా ప్రాక్స్‌కీ, ఈపాస్2003, ఎమ్-టోకెన్ అన్నీ టైప్-సి మరియు OTG లో పనిచేస్తాయి.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"Universal CCID: PROXKey, ePass2003, mToken.\"</i><br/><b>TE:</b> <i>\"ప్రాక్స్‌కీ, ఈపాస్2003, ఎమ్-టోకెన్ అన్నీ పనిచేస్తాయి.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q6: What if user enters wrong PIN 3 times?</b><br/>(3 సార్లు తప్పు పిన్ కొడితే ఏమవుతుంది?)", table_cell_q),
        Paragraph("Hardware locks automatically after 3-5 failed attempts (ISO 7816 `63 CX`), neutralizing brute-force attacks.", table_cell_eng),
        Paragraph("3 సార్లు తప్పుడు పిన్ ఎంటర్ చేస్తే హార్డ్‌వేర్ చిప్ ఆటోమేటిక్‌గా లాక్ అయిపోతుంది, దొంగతనాలకు తావుండదు.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"Hardware lockout after 3 failed PIN attempts.\"</i><br/><b>TE:</b> <i>\"3 సార్లు తప్పు పిన్ కొడితే టోకెన్ ఆటోమేటిక్‌గా లాక్ అవుతుంది.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q7: Does the dongle drain battery?</b><br/>(మొబైల్ బ్యాటరీ ఎక్కువగా ఖర్చవుతుందా?)", table_cell_q),
        Paragraph("Ultra-low power draw (<50mA active). Consumes less than 0.01% battery per signature.", table_cell_eng),
        Paragraph("చాలా తక్కువ కరెంట్ (<50mA) తీసుకుంటుంది; ఒక్క సంతకానికి 0.01% బ్యాటరీ కూడా ఖర్చుకాదు.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"<50mA ultra-low draw (<0.01% battery per sign).\"</i><br/><b>TE:</b> <i>\"చాలా తక్కువ పవర్, బ్యాటరీ ఏమాత్రం తగ్గదు.\"</i>", table_cell_sc_tel)
    ]
]
t_qc2 = Table(qa_c2, colWidths=[105, 145, 150, 150])
t_qc2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), SECONDARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
elements.append(t_qc2)

# PAGE BREAK
elements.append(PageBreak())

# SECTION 3: LEGAL & CCA INDIA COMPLIANCE (BILINGUAL)
elements.append(Paragraph("3. Legal, CCA India & Cryptographic Compliance (చట్టబద్ధత & నిబంధనలు)", h1_style))

qa_c3 = [
    [Paragraph("Question (ప్రశ్న)", table_header), Paragraph("English Technical Answer", table_header), Paragraph("తెలుగు సమాధానం (Telugu Answer)", table_header), Paragraph("⚡ 1-Line Shortcut (రెండు భాషలలో)", table_header)],
    [
        Paragraph("<b>Q8: Is it valid under IT Act 2000?</b><br/>(భారత IT చట్టం ప్రకారం చెల్లుతుందా?)", table_cell_q),
        Paragraph("<b>100% Legally Valid.</b> Complies with Section 3 & 3A of IT Act 2000 and CCA India rules, valid in all Indian Courts.", table_cell_eng),
        Paragraph("<b>100% చట్టబద్ధమైనది.</b> ఐటీ చట్టం సెక్షన్ 3 & 3A మరియు CCA నిబంధనల ప్రకారం భారతదేశంలోని అన్ని కోర్టులలో చెల్లుబాటు అవుతుంది.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"Fully compliant with IT Act 2000 Section 3/3A.\"</i><br/><b>TE:</b> <i>\"ఐటీ యాక్ట్ సెక్షన్ 3 & 3A ప్రకారం 100% చెల్లుబాటు అవుతుంది.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q9: Why Adobe shows Green Tick?</b><br/>(అడోబ్‌లో గ్రీన్ టిక్ మార్క్ ఎందుకు వస్తుంది?)", table_cell_q),
        Paragraph("Builds PAdES-LTV (ETSI EN 319 142) container with RFC 3161 TSA timestamp and embedded DSS validation.", table_cell_eng),
        Paragraph("PAdES-LTV మరియు టైమ్‌స్టాంప్ అంతర్గతంగా ఉండటం వల్ల అడోబ్ రీడర్‌లో అధికారిక గ్రీన్ టిక్ మార్క్ వస్తుంది.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"PAdES-LTV + RFC 3161 TSA guarantees Green Tick.\"</i><br/><b>TE:</b> <i>\"PAdES-LTV వల్ల అడోబ్‌లో అసలైన గ్రీన్ టిక్ వస్తుంది.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q10: What if certificate is revoked?</b><br/>(సర్టిఫికెట్ రద్దయితే ఏమవుతుంది?)", table_cell_q),
        Paragraph("Backend queries live OCSP and CRL responders during assembly. If revoked, signing is instantly blocked.", table_cell_eng),
        Paragraph("ఆన్‌లైన్ OCSP/CRL ద్వారా సర్టిఫికెట్ రద్దయిందో లేదో తనిఖీ చేసి, రద్దయిన సర్టిఫికెట్‌ను వెంటనే నిలిపివేస్తుంది.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"Live OCSP & CRL checks block revoked certs.\"</i><br/><b>TE:</b> <i>\"రద్దయిన సర్టిఫికెట్లను ఆటోమేటిక్‌గా బ్లాక్ చేస్తుంది.\"</i>", table_cell_sc_tel)
    ]
]
t_qc3 = Table(qa_c3, colWidths=[105, 145, 150, 150])
t_qc3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PURPLE),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
elements.append(t_qc3)
elements.append(Spacer(1, 3))

# SECTION 4: AP STATE INTEGRATION & PILOT (BILINGUAL)
elements.append(Paragraph("4. AP State Integration, Scalability & Pilot (ఏపీ ప్రభుత్వం & పైలట్ విస్తరణ)", h1_style))

qa_c4 = [
    [Paragraph("Question (ప్రశ్న)", table_header), Paragraph("English Technical Answer", table_header), Paragraph("తెలుగు సమాధానం (Telugu Answer)", table_header), Paragraph("⚡ 1-Line Shortcut (రెండు భాషలలో)", table_header)],
    [
        Paragraph("<b>Q11: How to integrate with AP e-Office?</b><br/>(ఏపీ ఈ-ఆఫీస్ తో ఎలా కలుపుతారు?)", table_cell_q),
        Paragraph("Via Android App Intent (e-Office invokes SecureSign and gets signed PDF back), REST APIs on APSDC, or embedded SDK.", table_cell_eng),
        Paragraph("ఆండ్రాయిడ్ యాప్ ఇంటెంట్ లేదా REST API ద్వారా ఏపీ ఈ-ఆఫీస్ మొబైల్ యాప్‌తో సులభంగా అనుసంధానించవచ్చు.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"Plug-and-play App Intent, REST API, or SDK.\"</i><br/><b>TE:</b> <i>\"ఆండ్రాయిడ్ ఇంటెంట్ లేదా REST API తో సులభంగా కనెక్ట్ చేయవచ్చు.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q12: Does it work in remote villages?</b><br/>(గ్రామాల్లో నెట్ లేకపోయినా పనిచేస్తుందా?)", table_cell_q),
        Paragraph("<b>YES.</b> Cryptographic signing between phone and token is 100% offline via local USB CCID. It auto-syncs when online.", table_cell_eng),
        Paragraph("<b>అవును!</b> మొబైల్-డోంగిల్ మధ్య సైనింగ్ 100% ఆఫ్‌లైన్‌లో జరుగుతుంది; ఇంటర్నెట్ రాగానే సర్వర్‌కి సింక్ అవుతుంది.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"100% Offline Signing on device + auto-sync.\"</i><br/><b>TE:</b> <i>\"ఇంటర్నెట్ లేకుండా 100% ఆఫ్‌లైన్ లోనే సంతకం పూర్తవుతుంది.\"</i>", table_cell_sc_tel)
    ],
    [
        Paragraph("<b>Q13: What is the Pilot Roadmap?</b><br/>(పైలట్ ప్రణాళిక ఏమిటి?)", table_cell_q),
        Paragraph("• Phase 1 (14 days): 50 Secretariat Secretaries.<br/>• Phase 2 (30 days): 26 District Collectorates.<br/>• Phase 3: Statewide expansion.", table_cell_eng),
        Paragraph("• 14 రోజుల్లో సెక్రటేరియట్ పైలట్ (50 మంది కార్యదర్శులు).<br/>• 30 రోజుల్లో 26 జిల్లాల కలెక్టరేట్లకు విస్తరణ.<br/>• ఆ తర్వాత రాష్ట్రవ్యాప్త విస్తరణ.", table_cell_tel),
        Paragraph("<b>EN:</b> <i>\"14-day Secretariat Pilot -> 30-day Collectorates.\"</i><br/><b>TE:</b> <i>\"14 రోజుల్లో సెక్రటేరియట్ పైలట్, 30 రోజుల్లో 26 జిల్లాల్లో విస్తరణ.\"</i>", table_cell_sc_tel)
    ]
]
t_qc4 = Table(qa_c4, colWidths=[105, 145, 150, 150])
t_qc4.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TEAL),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
elements.append(t_qc4)

# PAGE BREAK
elements.append(PageBreak())

# SECOND IMAGE: ACTIVITY STATE MACHINE
activity_img_path = 'uploads/SecureSign_Activity_Diagram.png'
if not os.path.exists(activity_img_path) and os.path.exists('SecureSign_Activity_Diagram.png'):
    activity_img_path = 'SecureSign_Activity_Diagram.png'

if os.path.exists(activity_img_path):
    elements.append(Paragraph("<b>SecureSign Activity State Machine / సిస్టమ్ యాక్టివిటీ ఫ్లోచార్ట్:</b>", h1_style))
    img_act = RLImage(activity_img_path, width=550, height=240)
    elements.append(img_act)
    elements.append(Spacer(1, 3))

# 4-STEP LIVE DEMO BOX (BILINGUAL)
elements.append(Paragraph("<b>4-Step Live Demo Formula / లైవ్ డెమోలో 4 సులభమైన దశలు:</b>", h1_style))
demo_b = [
    [
        Paragraph("<b>1. PLUG (కనెక్ట్)</b><br/>Plug Type-C Dongle into Phone.<br/><b>తెలుగు:</b> మొబైల్‌కు డోంగిల్ కనెక్ట్ చేయండి.", table_cell_q),
        Paragraph("<b>2. DETECT (గుర్తింపు)</b><br/>App shows Token & Cert details.<br/><b>తెలుగు:</b> యాప్ సర్టిఫికెట్ గుర్తిస్తుంది.", table_cell_q),
        Paragraph("<b>3. SIGN (సంతకం)</b><br/>Enter PIN -> Signs in 2 seconds.<br/><b>తెలుగు:</b> పిన్ కొట్టి 2 సెకన్లలో సైన్ చేయండి.", table_cell_q),
        Paragraph("<b>4. VERIFY (ధృవీకరణ)</b><br/>Open in Adobe -> Green Tick Valid.<br/><b>తెలుగు:</b> అడోబ్‌లో గ్రీన్ టిక్ చూపించండి.", table_cell_q)
    ]
]
t_db = Table(demo_b, colWidths=[137, 137, 137, 137])
t_db.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
    ('BOX', (0,0), (-1,-1), 1, GOLD),
    ('GRID', (0,0), (-1,-1), 0.5, GOLD),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
elements.append(t_db)
elements.append(Spacer(1, 3))

# EMERGENCY CONTINGENCY PLAN (BILINGUAL)
elements.append(Paragraph("<b>Emergency Backup Plan / అత్యవసర బ్యాకప్ ప్లాన్:</b>", h1_style))
em_data = [
    [
        Paragraph("<b>Scenario / సమస్య</b>", table_header),
        Paragraph("<b>Action / చేయవలసిన పని</b>", table_header),
        Paragraph("<b>What to Say / చెప్పవలసిన సమాధానం</b>", table_header)
    ],
    [
        Paragraph("Screen share lags on Google Meet<br/>(స్క్రీన్ షేర్ స్లో అయితే)", table_cell_q),
        Paragraph("Play backup video <code>SecureSign_Demonstration_Video.mp4</code> or show <code>test_signed_output.pdf</code> in Adobe.<br/>(బ్యాకప్ వీడియో లేదా అడోబ్ ఫైల్ చూపించండి)", table_cell_eng),
        Paragraph("<i>\"While the screen mirror reconnects, let me show you the verified signed PDF in Adobe Acrobat Reader.\"</i><br/>(స్క్రీన్ కనెక్ట్ అయ్యేలోపు అడోబ్‌లో వెరిఫై అయిన ఫైల్ చూపిస్తున్నాను.)", table_cell_tel)
    ],
    [
        Paragraph("Dongle not detected on first plug<br/>(డోంగిల్ వెంటనే కనెక్ట్ కాకపోతే)", table_cell_q),
        Paragraph("Unplug and replug firmly, accept Android USB permission prompt.<br/>(మరలా తీసి గట్టిగా పెట్టండి, USB పర్మిషన్ OK చేయండి)", table_cell_eng),
        Paragraph("<i>\"Android is establishing the secure CCID connection through the hardware USB bus.\"</i><br/>(ఆండ్రాయిడ్ సిస్టమ్ హార్డ్‌వేర్ USB కనెక్షన్‌ను ప్రారంభిస్తోంది.)", table_cell_tel)
    ]
]
t_em = Table(em_data, colWidths=[130, 210, 210])
t_em.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), RED),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD]),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
elements.append(t_em)

doc.build(elements)
shutil.copy(pdf_path, os.path.join('uploads', pdf_path))
print("Successfully generated Complete Bilingual PDF:", pdf_path)
