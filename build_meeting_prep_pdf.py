import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

os.makedirs('uploads', exist_ok=True)
pdf_path = 'SecureSign_Meeting_Demo_Preparation_Guide.pdf'

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Color Palette
PRIMARY = colors.HexColor('#0F172A')     # Slate 900
SECONDARY = colors.HexColor('#1E40AF')   # Blue 800
ACCENT = colors.HexColor('#0D9488')      # Teal 600
HIGHLIGHT = colors.HexColor('#DC2626')   # Red 600
GOLD = colors.HexColor('#D97706')        # Amber 600
BG_LIGHT = colors.HexColor('#F8FAFC')    # Slate 50
BG_CARD = colors.HexColor('#F1F5F9')     # Slate 100
BORDER_COLOR = colors.HexColor('#CBD5E1')# Slate 300
TEXT_DARK = colors.HexColor('#0F172A')
TEXT_MUTED = colors.HexColor('#475569')

# Typography Styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=PRIMARY,
    alignment=1,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=14,
    textColor=SECONDARY,
    alignment=1,
    spaceAfter=10
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12.5,
    leading=16,
    textColor=PRIMARY,
    spaceBefore=10,
    spaceAfter=5
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=SECONDARY,
    spaceBefore=6,
    spaceAfter=3
)

body_style = ParagraphStyle(
    'BodyDark',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11.5,
    textColor=TEXT_DARK
)

body_bold = ParagraphStyle(
    'BodyDarkBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11.5,
    textColor=TEXT_DARK
)

body_italic = ParagraphStyle(
    'BodyDarkItalic',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=8.5,
    leading=11.5,
    textColor=TEXT_MUTED
)

script_speak = ParagraphStyle(
    'ScriptSpeak',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor('#1E293B')
)

table_header = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    textColor=colors.white
)

table_cell = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=10.5,
    textColor=TEXT_DARK
)

table_cell_bold = ParagraphStyle(
    'TableCellBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10.5,
    textColor=TEXT_DARK
)

elements = []

# Title & Header
elements.append(Paragraph("SECURESIGN INNOVATION CHALLENGE", title_style))
elements.append(Paragraph("EVALUATION COMMITTEE LIVE DEMO & PITCH MASTER GUIDE", subtitle_style))
elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=8))

# Meeting Details Box
meeting_info_data = [
    [
        Paragraph("<b>Event:</b> Solution Demonstration & Evaluation", table_cell),
        Paragraph("<b>Date:</b> 08-09-2026 (Tomorrow)", table_cell_bold)
    ],
    [
        Paragraph("<b>Organizers:</b> Startup Andhra Pradesh / APIS (ITE&C Dept)", table_cell),
        Paragraph("<b>Time:</b> 11:30 AM – 12:30 PM IST (60 Mins)", table_cell_bold)
    ],
    [
        Paragraph("<b>Contact:</b> Madan Mohan Mohapatra (+91-9778627236)", table_cell),
        Paragraph("<b>VC Link:</b> <u>https://meet.google.com/cmz-hrzn-bvr</u>", table_cell_bold)
    ]
]

t_meet = Table(meeting_info_data, colWidths=[270, 270])
t_meet.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
    ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
    ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
elements.append(t_meet)
elements.append(Spacer(1, 8))

# SECTION 1: 1-HOUR MEETING TIMELINE & STRATEGY
elements.append(Paragraph("1. One-Hour Meeting Execution Timeline", h1_style))
timeline_data = [
    [Paragraph("Time Slot", table_header), Paragraph("Stage", table_header), Paragraph("Key Goal & Action Items", table_header)],
    [
        Paragraph("<b>11:30 - 11:35 AM</b><br/>(5 Mins)", table_cell),
        Paragraph("<b>Welcome & Setup</b>", table_cell_bold),
        Paragraph("Join 10 mins early (11:20 AM). Test audio/video, share screen smoothly, introduce the team, thank AP Innovation Society & ITE&C Dept.", table_cell)
    ],
    [
        Paragraph("<b>11:35 - 11:47 AM</b><br/>(12 Mins)", table_cell),
        Paragraph("<b>Slide Deck Pitch</b>", table_cell_bold),
        Paragraph("Present Executive Slides: The Problem (Desktop dependency for DSC), The Architecture (CCID native driver + PKCS#11), Compliance (CCA India / IT Act 2000), and AP e-Governance benefits.", table_cell)
    ],
    [
        Paragraph("<b>11:47 - 12:05 PM</b><br/>(18 Mins)", table_cell),
        Paragraph("<b>Live Solution Demo</b>", table_cell_bold),
        Paragraph("<b>CRITICAL STAGE:</b> Plug in Type-C DSC dongle -> Show device detection -> Select AP Government Order PDF -> Enter PIN -> Instant native cryptographic signing -> Open signed PDF in Adobe Reader with Green Checkmark.", table_cell)
    ],
    [
        Paragraph("<b>12:05 - 12:25 PM</b><br/>(20 Mins)", table_cell),
        Paragraph("<b>Technical Defense & Q&A</b>", table_cell_bold),
        Paragraph("Answer technical questions from IAS Officers / Technical Evaluators regarding security, private key isolation, dongle compatibility, and integration with AP e-Office / CFMS.", table_cell)
    ],
    [
        Paragraph("<b>12:25 - 12:30 PM</b><br/>(5 Mins)", table_cell),
        Paragraph("<b>Closing & Pilot Plan</b>", table_cell_bold),
        Paragraph("Propose immediate 2-week pilot deployment for AP Secretariat & District Collectorates. Express commitment to digital governance in Andhra Pradesh.", table_cell)
    ]
]
t_time = Table(timeline_data, colWidths=[90, 120, 330])
t_time.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
elements.append(t_time)
elements.append(Spacer(1, 8))

# SECTION 2: STEP-BY-STEP LIVE DEMONSTRATION WORKFLOW
elements.append(Paragraph("2. Step-by-Step Live Demo Execution Protocol", h1_style))
demo_steps = [
    [Paragraph("#", table_header), Paragraph("Step Description", table_header), Paragraph("What the Panel Sees on Screen", table_header), Paragraph("Key Talking Point to Emphasize", table_header)],
    [
        Paragraph("<b>1</b>", table_cell),
        Paragraph("<b>Launch App</b>", table_cell_bold),
        Paragraph("SecureSign Mobile dashboard loading on Android device.", table_cell),
        Paragraph("Zero third-party bridge required. 100% native Android runtime.", table_cell)
    ],
    [
        Paragraph("<b>2</b>", table_cell),
        Paragraph("<b>Connect Dongle</b>", table_cell_bold),
        Paragraph("Plug Type-C DSC (or OTG Dongle) into phone. Android USB prompt appears: <i>'Allow SecureSign to access USB device?'</i>", table_cell),
        Paragraph("Direct USB CCID (Class 0x0B) Host communication via Kotlin driver.", table_cell)
    ],
    [
        Paragraph("<b>3</b>", table_cell),
        Paragraph("<b>Dongle Detection</b>", table_cell_bold),
        Paragraph("App shows <b>'Token Connected'</b> with Certificate details (Signer Name, Issuer CA eMudhra/VSign, Validity).", table_cell),
        Paragraph("X.509 Certificate public metadata read directly via APDU ISO 7816-4.", table_cell)
    ],
    [
        Paragraph("<b>4</b>", table_cell),
        Paragraph("<b>Select Document</b>", table_cell_bold),
        Paragraph("Choose sample file: <i>'G.O. Ms. No. 104 - AP ITE&C Dept Approval Order'</i>.", table_cell),
        Paragraph("Integrated viewer renders PDF without cloud upload (data privacy intact).", table_cell)
    ],
    [
        Paragraph("<b>5</b>", table_cell),
        Paragraph("<b>Enter User PIN</b>", table_cell_bold),
        Paragraph("Secure PIN dialog pops up. Enter token PIN (e.g. 12345678).", table_cell),
        Paragraph("Hardware-level PIN verification with attempt lockout protection.", table_cell)
    ],
    [
        Paragraph("<b>6</b>", table_cell),
        Paragraph("<b>Hardware Signing</b>", table_cell_bold),
        Paragraph("Press <b>'Sign Document'</b> -> Progress indicator -> Signed in < 2.5s.", table_cell),
        Paragraph("<b>Crucial:</b> Private key NEVER leaves token. Only SHA-256 hash is signed.", table_cell)
    ],
    [
        Paragraph("<b>7</b>", table_cell),
        Paragraph("<b>Verification Proof</b>", table_cell_bold),
        Paragraph("Open signed PDF in Adobe Acrobat / PDF Reader -> Signature Panel displays <b>'Signature is Valid'</b> with Green Tick.", table_cell),
        Paragraph("Full PAdES-LTV (ETSI EN 319 142) & RFC 3161 TSA Timestamp compliant.", table_cell)
    ]
]
t_demo = Table(demo_steps, colWidths=[20, 100, 210, 210])
t_demo.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), SECONDARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_demo)

# PAGE BREAK TO KEEP SCRIPT & Q&A CLEAN
elements.append(PageBreak())

# SECTION 3: WORD-FOR-WORD PITCH & DEMO SCRIPT
elements.append(Paragraph("3. Word-for-Word Presentation & Demo Script", h1_style))
elements.append(Paragraph("Use this exact script during the demonstration for confident, authoritative delivery:", body_italic))
elements.append(Spacer(1, 4))

script_data = [
    [
        Paragraph("<b>PHASE</b>", table_header),
        Paragraph("<b>VERBATIM SCRIPT (WHAT YOU SHOULD SAY)</b>", table_header)
    ],
    [
        Paragraph("<b>Opening & Greeting</b><br/>(1 Min)", table_cell_bold),
        Paragraph(
            "<i>\"Respected Committee Members, Evaluators, and Officers from the Andhra Pradesh Innovation Society and ITE&C Department, Good morning. I am thrilled to present <b>SecureSign</b>—our groundbreaking mobile digital signature solution designed specifically to empower Andhra Pradesh's digital governance ecosystem. Today, state officers are tethered to desktop PCs just to sign official G.O.s and files with USB DSC tokens. SecureSign brings true mobility to leadership by allowing Class 3 cryptographic signing directly on Android mobile devices with 100% legal compliance and zero security compromises.\"</i>",
            script_speak
        )
    ],
    [
        Paragraph("<b>Architecture Pitch</b><br/>(4 Mins)", table_cell_bold),
        Paragraph(
            "<i>\"Our core innovation lies in our <b>Native USB CCID Driver</b>. Unlike traditional systems that require cumbersome desktop bridges or proprietary cloud servers, SecureSign communicates directly with the physical USB Type-C crypto dongle using ISO 7816-4 APDU commands. The cryptographic private key is locked inside the FIPS 140-2 Level 3 / CC EAL 5+ hardware secure element. When signing, our app computes a SHA-256 document hash, sends only the 32-byte hash to the token, and receives the RSA-2048/4096 digital signature. The private key never leaves the hardware dongle at any moment.\"</i>",
            script_speak
        )
    ],
    [
        Paragraph("<b>Live Demo Walkthrough</b><br/>(10 Mins)", table_cell_bold),
        Paragraph(
            "<i>\"Let me demonstrate this live. (Screen share mobile screen). Here is our SecureSign application. I am now plugging in this Type-C DSC dongle. Notice how the app immediately detects the token and reads the X.509 certificate details issued by eMudhra. Next, I will select an official Andhra Pradesh Government Order. I review the document, tap 'Sign Document', and enter the secure hardware PIN. In less than 2 seconds, the cryptographic signature is assembled, stamped with an RFC 3161 timestamp, and embedded into a PAdES-LTV container. Opening this in Adobe Acrobat confirms the signature validity with the legally recognized Green Checkmark.\"</i>",
            script_speak
        )
    ],
    [
        Paragraph("<b>Closing & Pilot Offer</b><br/>(2 Mins)", table_cell_bold),
        Paragraph(
            "<i>\"SecureSign is fully compliant with Section 3 & 3A of the Indian IT Act 2000 and CCA India guidelines. Our APK is production-ready, supporting all major dongle vendors (WatchData ProxKey, ePass2003, mToken, SafeNet). We are ready to initiate an immediate 2-week pilot rollout for the AP Secretariat and District Collectorates. Thank you, and we welcome your questions.\"</i>",
            script_speak
        )
    ]
]

t_script = Table(script_data, colWidths=[100, 440])
t_script.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
elements.append(t_script)
elements.append(Spacer(1, 8))

# SECTION 4: TOP 8 EVALUATION PANEL QUESTIONS & DEFENSE
elements.append(Paragraph("4. Evaluation Committee Q&A Defense Master Sheet", h1_style))
elements.append(Paragraph("Be prepared to answer these exact technical and administrative questions from the panel:", body_italic))
elements.append(Spacer(1, 4))

qa_data = [
    [Paragraph("Panel Question", table_header), Paragraph("Winning Technical Answer & Key Defense Points", table_header)],
    [
        Paragraph("<b>Q1: Does the Private Key ever leave the USB Dongle or get uploaded to the cloud?</b>", table_cell_bold),
        Paragraph("<b>ABSOLUTELY NEVER.</b> The private key is non-exportable, locked in the FIPS 140-2 Level 3 / CC EAL 5+ Secure Element. The app only sends the SHA-256 document hash to the token via APDU commands. The cryptographic signing takes place purely on-chip inside the physical hardware.", table_cell)
    ],
    [
        Paragraph("<b>Q2: Is this legally valid under CCA India and the IT Act 2000?</b>", table_cell_bold),
        Paragraph("<b>YES.</b> It fulfills all requirements of Section 3 & 3A of the Indian IT Act 2000. It produces standard PAdES-LTV (ETSI EN 319 142) signatures and incorporates RFC 3161 TSA timestamps, ensuring universal validity in Adobe Reader and Indian courts.", table_cell)
    ],
    [
        Paragraph("<b>Q3: What USB Dongle brands & models are supported?</b>", table_cell_bold),
        Paragraph("Compatible with all CCA-approved USB tokens in India, including: <b>WatchData PROXKey</b>, <b>Feitian ePass 2003</b>, <b>mToken CryptoID</b>, <b>SafeNet eToken 5110</b>, and <b>HyperPKI</b> via standard CCID Class 0x0B.", table_cell)
    ],
    [
        Paragraph("<b>Q4: How does this integrate with AP e-Office, CFMS, or Spandana?</b>", table_cell_bold),
        Paragraph("SecureSign provides REST APIs, Android Intent SDKs, and deep-linking hooks. When an officer approves a file in AP e-Office Mobile, it triggers SecureSign via standard App Link, completes the hardware signature, and returns the signed PDF payload back to e-Office.", table_cell)
    ],
    [
        Paragraph("<b>Q5: What happens if an unauthorized person tries entering wrong PINs?</b>", table_cell_bold),
        Paragraph("Hardware-enforced security: The cryptographic token locks automatically after 3 to 5 failed PIN attempts, completely neutralizing brute-force attempts. Unlocking requires the official PUK/Admin credentials.", table_cell)
    ],
    [
        Paragraph("<b>Q6: Can signing work in rural areas with poor or zero internet connectivity?</b>", table_cell_bold),
        Paragraph("<b>YES.</b> The core cryptographic signing is performed 100% offline via local USB CCID communication between the phone and dongle. Internet is only required when fetching or submitting files to the remote server.", table_cell)
    ],
    [
        Paragraph("<b>Q7: Does the Android phone need Root access or Developer Mode?</b>", table_cell_bold),
        Paragraph("<b>NO.</b> SecureSign uses standard Android USB Host APIs (`android.hardware.usb`). It works out-of-the-box on standard consumer and government-issued Android smartphones (Android 8.0 to Android 15).", table_cell)
    ],
    [
        Paragraph("<b>Q8: What is your deployment readiness for Andhra Pradesh?</b>", table_cell_bold),
        Paragraph("The standalone APK is compiled, backend containerized on Docker, and end-to-end verified. We can deploy a 2-week pilot for 50+ Secretariat officers within 48 hours.", table_cell)
    ]
]

t_qa = Table(qa_data, colWidths=[180, 360])
t_qa.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), SECONDARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
elements.append(t_qa)

# PAGE BREAK FOR CHECKLIST & CONTACTS
elements.append(PageBreak())

# SECTION 5: PRE-MEETING SETUP & EMERGENCY BACKUP PROTOCOL
elements.append(Paragraph("5. Pre-Meeting Setup Checklist & Contingency Plan", h1_style))
elements.append(Paragraph("Complete these preparations today and 30 minutes before 11:30 AM tomorrow:", body_italic))
elements.append(Spacer(1, 4))

check_data = [
    [Paragraph("Item / Action", table_header), Paragraph("Preparation Steps & Contingency Action", table_header), Paragraph("Status", table_header)],
    [
        Paragraph("<b>1. Screen Mirroring Setup</b>", table_cell_bold),
        Paragraph("Connect Android phone to PC via USB using <b>Scrcpy</b> or join Google Meet from both PC (audio/camera) and Phone (screen share).", table_cell),
        Paragraph("<font color='green'><b>READY</b></font>", table_cell)
    ],
    [
        Paragraph("<b>2. Physical Hardware</b>", table_cell_bold),
        Paragraph("Ensure Type-C DSC Dongle / USB-A to Type-C OTG connector is ready, clean, and tested with PIN handy.", table_cell),
        Paragraph("<font color='green'><b>READY</b></font>", table_cell)
    ],
    [
        Paragraph("<b>3. Presentation Slides</b>", table_cell_bold),
        Paragraph("Have <i>'SecureSign_Executive_Master_Deck_2026.pptx'</i> or HTML presentation open in full screen on your computer.", table_cell),
        Paragraph("<font color='green'><b>READY</b></font>", table_cell)
    ],
    [
        Paragraph("<b>4. Backup Demo Video</b>", table_cell_bold),
        Paragraph("Have <i>'SecureSign_Demonstration_Video.mp4'</i> ready in VLC/Media Player in case physical screen share experiences lag.", table_cell),
        Paragraph("<font color='green'><b>READY</b></font>", table_cell)
    ],
    [
        Paragraph("<b>5. Pre-Signed Sample PDFs</b>", table_cell_bold),
        Paragraph("Keep <i>'test_signed_output.pdf'</i> and <i>'SecureSign_Sample_Signed_Document.pdf'</i> open in Adobe Acrobat to show green checkmark instantly.", table_cell),
        Paragraph("<font color='green'><b>READY</b></font>", table_cell)
    ],
    [
        Paragraph("<b>6. Meeting Environment</b>", table_cell_bold),
        Paragraph("Ensure quiet room, stable high-speed Wi-Fi, wired earphone/microphone, and join Google Meet at 11:20 AM.", table_cell),
        Paragraph("<font color='green'><b>READY</b></font>", table_cell)
    ]
]

t_chk = Table(check_data, colWidths=[140, 330, 70])
t_chk.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('ALIGN', (2,1), (2,-1), 'CENTER')
]))
elements.append(t_chk)
elements.append(Spacer(1, 10))

# Quick Contact & Reference Box
elements.append(Paragraph("6. Important Meeting & Organizer Reference", h1_style))
ref_data = [
    [
        Paragraph("<b>Official Meeting Details:</b><br/>• <b>Google Meet Link:</b> <font color='#1E40AF'><u>https://meet.google.com/cmz-hrzn-bvr</u></font><br/>• <b>Scheduled Date & Time:</b> 08-09-2026 at 11:30 AM – 12:30 PM IST<br/>• <b>Evaluation Body:</b> Andhra Pradesh Innovation Society (APIS) & ITE&C Dept, Govt. of AP", table_cell),
        Paragraph("<b>Key Organizer Contact:</b><br/>• <b>Officer:</b> Madan Mohan Mohapatra (Manager - Investment & Partnerships)<br/>• <b>Mobile:</b> +91-9778627236<br/>• <b>Email:</b> startupmanager2-apis@ap.gov.in<br/>• <b>Official Portal:</b> www.apis.ap.gov.in", table_cell)
    ]
]
t_ref = Table(ref_data, colWidths=[270, 270])
t_ref.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
    ('BOX', (0,0), (-1,-1), 1, SECONDARY),
    ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
elements.append(t_ref)

doc.build(elements)

# Copy to uploads as well
shutil.copy(pdf_path, os.path.join('uploads', pdf_path))
print("Successfully generated:", pdf_path)
