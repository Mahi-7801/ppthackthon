import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout_box(doc, eng_text, tel_text, title=""):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "FEF3C7") # Amber 100
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        run_title = p.add_run(f"📌 {title}\n")
        run_title.font.name = "Segoe UI"
        run_title.font.bold = True
        run_title.font.size = Pt(10)
        run_title.font.color.rgb = RGBColor(146, 64, 14) # Amber 800
    
    if eng_text:
        run_eng = p.add_run(f"🇬🇧 English: {eng_text}\n")
        run_eng.font.name = "Segoe UI"
        run_eng.font.bold = True
        run_eng.font.size = Pt(9.5)
        run_eng.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        
    if tel_text:
        run_tel = p.add_run(f"🇮🇳 తెలుగు (Telugu): {tel_text}")
        run_tel.font.name = "Nirmala UI"
        run_tel.font.bold = True
        run_tel.font.size = Pt(9.5)
        run_tel.font.color.rgb = RGBColor(6, 95, 70) # Emerald 800

def create_document():
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)
        
    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    run_t = p_title.add_run("SECURESIGN INNOVATION CHALLENGE 2026")
    run_t.font.name = "Segoe UI"
    run_t.font.bold = True
    run_t.font.size = Pt(16)
    run_t.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(6)
    run_s = p_sub.add_run("Evaluation Committee Live Demo & Technical Defense Master Guide\nసెక్యూర్‌సైన్ — మూల్యాంకన కమిటీ సమగ్ర డెమో & టెక్నికల్ గైడ్ (English & తెలుగు)")
    run_s.font.name = "Nirmala UI"
    run_s.font.bold = True
    run_s.font.size = Pt(10.5)
    run_s.font.color.rgb = RGBColor(30, 64, 175) # Royal Blue
    
    # Meeting Details Box
    t_meet = doc.add_table(rows=2, cols=2)
    t_meet.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row in t_meet.rows:
        for cell in row.cells:
            set_cell_background(cell, "F1F5F9") # Slate 100
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            
    c00 = t_meet.cell(0, 0).paragraphs[0]
    r = c00.add_run("📅 Date & Time / తేదీ & సమయం:\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r2 = c00.add_run("08-09-2026 (Tomorrow) | 11:30 AM – 12:30 PM IST")
    r2.font.size = Pt(9)
    
    c01 = t_meet.cell(0, 1).paragraphs[0]
    r = c01.add_run("🔗 Google Meet Link / మీటింగ్ లింక్:\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r2 = c01.add_run("https://meet.google.com/cmz-hrzn-bvr")
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(30, 64, 175)
    r2.font.size = Pt(9)
    
    c10 = t_meet.cell(1, 0).paragraphs[0]
    r = c10.add_run("🏛️ Organizers / నిర్వాహకులు:\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r2 = c10.add_run("Startup Andhra Pradesh & AP Innovation Society (ITE&C Dept)")
    r2.font.size = Pt(9)
    
    c11 = t_meet.cell(1, 1).paragraphs[0]
    r = c11.add_run("👤 Nodal Officer / నోడల్ అధికారి:\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r2 = c11.add_run("Madan Mohan Mohapatra (+91-9778627236 | startupmanager2-apis@ap.gov.in)")
    r2.font.size = Pt(9)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Workflow Image
    img_path = 'uploads/SecureSign_Executive_Workflow_Diagram.png'
    if not os.path.exists(img_path) and os.path.exists('SecureSign_Executive_Workflow_Diagram.png'):
        img_path = 'SecureSign_Executive_Workflow_Diagram.png'
        
    if os.path.exists(img_path):
        p_img_title = doc.add_paragraph()
        p_img_title.paragraph_format.space_before = Pt(4)
        p_img_title.paragraph_format.space_after = Pt(2)
        r = p_img_title.add_run("📊 End-to-End Visual Workflow Timeline / ఎండ్-టు-ఎండ్ ఆర్కిటెక్చర్ ఫ్లో:")
        r.font.name = "Nirmala UI"
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(15, 23, 42)
        
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_path, width=Inches(6.8))
        
    # 5-Stage Timeline Table
    t_stage = doc.add_table(rows=6, cols=3)
    t_stage.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Stage / దశ", "🇬🇧 English Technical Workflow", "🇮🇳 తెలుగు పూర్తి వివరణ (Telugu Flow)"]
    for i, h in enumerate(headers):
        cell = t_stage.cell(0, i)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Nirmala UI"
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    stages_content = [
        (
            "Stage 1: Ingestion\n(డాక్యుమెంట్ ఎంపిక)",
            "Officer selects G.O. PDF on Mobile; App streams 64KB chunks to calculate local SHA-256 digest (<100ms).",
            "అధికారి మొబైల్‌లో PDF ఫైల్ ఎంచుకోగానే, యాప్ మెమరీ లీక్ లేకుండా 64KB చంక్స్‌తో స్థానికంగా SHA-256 హాష్ జనరేట్ చేస్తుంది."
        ),
        (
            "Stage 2: USB Handshake\n(డోంగిల్ కనెక్షన్)",
            "Native Kotlin driver negotiates USB CCID Class 0x0B over bulk endpoints; reads X.509 certificate (<350ms).",
            "మొబైల్ ఆండ్రాయిడ్ స్థానిక USB CCID డ్రైవర్ ద్వారా డోంగిల్‌ను గుర్తించి, eMudhra X.509 సర్టిఫికెట్ వివరాలు లోడ్ చేస్తుంది."
        ),
        (
            "Stage 3: Hardware Sign\n(హార్డ్‌వేర్ సంతకం)",
            "User enters PIN; APDU passes 32-byte digest into CC EAL 5+ crypto chip; signs purely on-hardware (<800ms).",
            "పిన్ ఎంటర్ చేయగానే ప్రైవేట్ కీ బయటకు రాకుండా, హార్డ్‌వేర్ చిప్ లోపలే సురక్షితంగా క్రిప్టోగ్రాఫిక్ సంతకం పూర్తవుతుంది."
        ),
        (
            "Stage 4: PAdES-LTV\n(టైమ్‌స్టాంప్ భద్రత)",
            "Assembles signature with RFC 3161 TSA Timestamp token & embedded DSS revocation store for 20+ years (<450ms).",
            "సంతకానికి అధికారిక RFC 3161 టైమ్‌స్టాంప్ జతచేసి, భవిష్యత్తులో 20+ ఏళ్ల పాటు చెల్లుబాటు అయ్యేలా PAdES-LTV ఫార్మాట్ చేస్తుంది."
        ),
        (
            "Stage 5: Verification\n(గ్రీన్ టిక్ మార్క్)",
            "Signed PDF opened in Adobe Acrobat Reader; displays instant legally binding 'Signature is Valid' Green Tick.",
            "సంతకం పూర్తయిన ఫైల్‌ను అడోబ్ రీడర్‌లో తెరవగానే చట్టబద్ధమైన ఆకుపచ్చ టిక్ మార్క్ (Green Tick) తో ధృవీకరించబడుతుంది."
        )
    ]
    
    for row_idx, (st, eng, tel) in enumerate(stages_content, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F8FAFC"
        row = t_stage.rows[row_idx]
        
        # Col 0
        c0 = row.cells[0]
        set_cell_background(c0, bg)
        set_cell_margins(c0, top=80, bottom=80, left=120, right=120)
        p0 = c0.paragraphs[0]
        r = p0.add_run(st)
        r.font.name = "Nirmala UI"
        r.font.bold = True
        r.font.size = Pt(8.5)
        
        # Col 1
        c1 = row.cells[1]
        set_cell_background(c1, bg)
        set_cell_margins(c1, top=80, bottom=80, left=120, right=120)
        p1 = c1.paragraphs[0]
        r = p1.add_run(eng)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        
        # Col 2
        c2 = row.cells[2]
        set_cell_background(c2, bg)
        set_cell_margins(c2, top=80, bottom=80, left=120, right=120)
        p2 = c2.paragraphs[0]
        r = p2.add_run(tel)
        r.font.name = "Nirmala UI"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(6, 95, 70)
        
    doc.add_page_break()
    
    # MASTER QUESTION BANK (BILINGUAL PARALLEL CARDS)
    p_sec = doc.add_paragraph()
    r = p_sec.add_run("MASTER JURY DEFENSE & TECHNICAL QUESTION BANK (20+ Q&As)\nప్రశ్నలు, సమాధానాలు మరియు షార్ట్‌కట్స్ (English & తెలుగు)")
    r.font.name = "Nirmala UI"
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    categories = [
        {
            "cat_title": "Category 1: Coding, Internal Architecture & Native Drivers (కోడింగ్ & ఆర్కిటెక్చర్)",
            "color": "1E40AF",
            "questions": [
                {
                    "q_num": "Q1",
                    "q_eng": "How does the mobile app talk to the USB dongle without root access?",
                    "q_tel": "రూట్ పర్మిషన్స్ లేకుండా మొబైల్ డోంగిల్‌తో ఎలా కమ్యూనికేట్ చేస్తుంది?",
                    "sc_eng": "\"Native Kotlin USB CCID Driver (Class 0x0B) via standard bulk endpoints with zero root.\"",
                    "sc_tel": "\"ఎలాంటి రూట్ లేకుండా నేటివ్ ఆండ్రాయిడ్ USB CCID డ్రైవర్ ద్వారా నేరుగా పనిచేస్తుంది.\"",
                    "ans_eng": "We built a custom Kotlin CCID USB Driver utilizing Android's standard android.hardware.usb.UsbManager. It establishes a UsbDeviceConnection directly to the Smart Card interface (Class 0x0B) and executes ISO/IEC 7816-4 APDU command frames over native bulk endpoints.",
                    "ans_tel": "మేము ఆండ్రాయిడ్ స్థానిక UsbManager ద్వారా ప్రత్యేకమైన కోట్లిన్ CCID డ్రైవర్‌ను నిర్మించాము. ఇది క్లాస్ 0x0B స్మార్ట్ కార్డ్ ఇంటర్‌ఫేస్ ద్వారా ISO 7816-4 APDU కమాండ్లను నేరుగా బల్క్ ఎండ్‌పాయింట్లపై నడుపుతుంది."
                },
                {
                    "q_num": "Q2",
                    "q_eng": "Does the Private Key ever leave the USB dongle or get uploaded anywhere?",
                    "q_tel": "ప్రైవేట్ కీ ఎప్పుడైనా డోంగిల్ నుండి బయటకు వస్తుందా లేదా క్లౌడ్‌కి అప్‌లోడ్ అవుతుందా?",
                    "sc_eng": "\"Private key NEVER leaves the token; only the 32-byte SHA-256 hash is signed on-chip.\"",
                    "sc_tel": "\"ప్రైవేట్ కీ ఎప్పటికీ బయటకు రాదు; కేవలం 32-బైట్ల హాష్ మాత్రమే చిప్ లోపల సైన్ అవుతుంది.\"",
                    "ans_eng": "ABSOLUTELY NEVER. The private key is non-exportable, permanently isolated inside the FIPS 140-2 Level 3 / CC EAL 5+ hardware secure element. The mobile app only sends the 32-byte SHA-256 document hash via APDU (00 2A 9E 9A); the signature is calculated purely on-hardware.",
                    "ans_tel": "ఎట్టిపరిస్థితుల్లోనూ బయటకు రాదు. ప్రైవేట్ కీ FIPS 140-2 Level 3 / CC EAL 5+ హార్డ్‌వేర్ క్రిప్టో చిప్‌లోనే లాక్ అయి ఉంటుంది. మొబైల్ యాప్ కేవలం డాక్యుమెంట్ యొక్క 32-బైట్ల SHA-256 హాష్‌ను మాత్రమే పంపిస్తుంది."
                },
                {
                    "q_num": "Q3",
                    "q_eng": "What is the complete Tech Stack across Mobile and Backend?",
                    "q_tel": "మొబైల్ మరియు బ్యాకెండ్‌లో ఉపయోగించిన పూర్తి టెక్నాలజీ స్టాక్ ఏమిటి?",
                    "sc_eng": "\"React Native for UI + Native Kotlin for USB CCID Driver + Node.js for PAdES-LTV.\"",
                    "sc_tel": "\"రియాక్ట్ నేటివ్ (UI) + నేటివ్ కోట్లిన్ (USB డ్రైవర్) + నోడ్.జేఎస్ (PAdES ఇంజిన్).\"",
                    "ans_eng": "• Mobile UI: React Native 0.74 + TypeScript for fluid, cross-platform performance.\n• Native Hardware Engine: Kotlin/Java Native Module (DSCSigningModule) for USB CCID & APDU.\n• Backend & TSA: Node.js + Express with PKCS#7 / PAdES-LTV container assembly.\n• Containerization: Docker container deployed on Linux / State Data Center.",
                    "ans_tel": "• మొబైల్ యూజర్ ఇంటర్‌ఫేస్: రియాక్ట్ నేటివ్ 0.74 + టైప్‌స్క్రిప్ట్.\n• హార్డ్‌వేర్ డ్రైవర్ కోర్: నేటివ్ కోట్లిన్ USB మాడ్యూల్ (DSCSigningModule).\n• బ్యాకెండ్ & టైమ్‌స్టాంప్: నోడ్.జేఎస్ + ఎక్స్‌ప్రెస్ PAdES-LTV ఇంజిన్.\n• డిప్లాయ్‌మెంట్: డాకర్ కంటైనర్ (రాష్ట్ర డేటా సెంటర్ / APSDC కోసం సిద్ధం)."
                },
                {
                    "q_num": "Q4",
                    "q_eng": "How do you handle 100-page large Government Orders without memory lag?",
                    "q_tel": "100 పేజీల పెద్ద ప్రభుత్వ ఆర్డర్ (G.O.) ఫైళ్లను మెమరీ ల్యాగ్ లేకుండా ఎలా సైన్ చేస్తారు?",
                    "sc_eng": "\"64KB chunked stream hashing keeps RAM under 45MB with <2.5s signing speed.\"",
                    "sc_tel": "\"64KB స్ట్రీమింగ్ హాషింగ్ వల్ల 45MB ర్యామ్‌తో 100 పేజీల ఫైల్ కూడా 2.5 సెకన్లలో సైన్ అవుతుంది.\"",
                    "ans_eng": "We implement 64KB chunked stream hashing. The entire PDF is never loaded into RAM at once; hashes are computed iteratively in streaming byte buffers, keeping peak runtime RAM at ~45MB and overall signing speed under 2.5 seconds.",
                    "ans_tel": "మేము 64KB స్ట్రీమింగ్ బఫర్ ఆర్కిటెక్చర్‌ను ఉపయోగించాము. మొత్తం PDF ఒకేసారి ర్యామ్‌లోకి లోడ్ అవ్వకుండా విడతలవారీగా హాష్ అవుతుంది. దీనివల్ల ర్యామ్ కేవలం 45MB మాత్రమే వాడుతూ 2.5 సెకన్లలో సైనింగ్ పూర్తవుతుంది."
                }
            ]
        },
        {
            "cat_title": "Category 2: Hardware, Dongles & Power Management (హార్డ్‌వేర్ & డోంగిల్స్)",
            "color": "0D9488",
            "questions": [
                {
                    "q_num": "Q5",
                    "q_eng": "Which USB dongle brands and models are supported?",
                    "q_tel": "ఏయే కంపెనీల క్రిప్టో డోంగిల్స్ సెక్యూర్‌సైన్‌లో పనిచేస్తాయి?",
                    "sc_eng": "\"Universal CCID support for WatchData PROXKey, ePass2003, mToken, and SafeNet.\"",
                    "sc_tel": "\"వాచ్‌డేటా ప్రాక్స్‌కీ, ఈపాస్2003, ఎమ్-టోకెన్ మరియు సేఫ్‌నెట్ అన్నీ పనిచేస్తాయి.\"",
                    "ans_eng": "Supports all CCA India-approved CCID tokens: WatchData PROXKey (widely used in AP Secretariat), Feitian ePass 2003 / Auto, mToken CryptoID, SafeNet eToken 5110, and HyperPKI via Type-C or OTG adapter.",
                    "ans_tel": "ఆంధ్రప్రదేశ్ సచివాలయంలో ఉపయోగించే వాచ్‌డేటా ప్రాక్స్‌కీ, ఈపాస్ 2003, ఎమ్-టోకెన్ క్రిప్టోఐడీ మరియు సేఫ్‌నెట్ ఈ-టోకెన్ వంటి అన్ని CCA గుర్తింపు పొందిన టోకెన్లు నేరుగా టైప్-సి లేదా OTG ద్వారా పనిచేస్తాయి."
                },
                {
                    "q_num": "Q6",
                    "q_eng": "What happens if an unauthorized person enters the wrong PIN 3 times?",
                    "q_tel": "ఎవరైనా తప్పుడు పిన్ (Wrong PIN) 3 సార్లు ఎంటర్ చేస్తే ఏమవుతుంది?",
                    "sc_eng": "\"Hardware lockout after 3 failed PIN attempts, neutralizing all brute-force attacks.\"",
                    "sc_tel": "\"3 సార్లు తప్పు పిన్ కొడితే హార్డ్‌వేర్ టోకెన్ ఆటోమేటిక్‌గా లాక్ అయిపోతుంది.\"",
                    "ans_eng": "Hardware-enforced security: The physical token firmware automatically blocks access after 3 to 5 failed attempts (ISO 7816 status 63 CX). Unlocking requires authorized PUK / Admin credentials, neutralizing brute-force threats completely.",
                    "ans_tel": "హార్డ్‌వేర్ భద్రతా నిబంధనల ప్రకారం: వరుసగా 3 సార్లు తప్పుడు పిన్ ఎంటర్ చేస్తే టోకెన్ చిప్ ఆటోమేటిక్‌గా లాక్ అయిపోతుంది. దీనివల్ల ఎలాంటి హ్యాకింగ్ లేదా దొంగతనాలకు అవకాశం ఉండదు."
                },
                {
                    "q_num": "Q7",
                    "q_eng": "Does the USB crypto dongle drain the smartphone's battery?",
                    "q_tel": "మొబైల్‌కి డోంగిల్ కనెక్ట్ చేయడం వల్ల బ్యాటరీ ఎక్కువగా ఖర్చవుతుందా?",
                    "sc_eng": "\"Ultra-low power draw (<50mA), consuming less than 0.01% battery per signature.\"",
                    "sc_tel": "\"చాలా తక్కువ కరెంట్ (<50mA), ఒక్క సంతకానికి 0.01% బ్యాటరీ కూడా ఖర్చుకాదు.\"",
                    "ans_eng": "No. Modern crypto tokens consume <50mA during active APDU signing and <5mA in idle mode. Signing one Government Order consumes less than 0.01% of a standard 5000mAh mobile battery.",
                    "ans_tel": "లేదు. క్రిప్టో డోంగిల్స్ చాలా తక్కువ పవర్ (<50mA) మాత్రమే తీసుకుంటాయి. ఒక డాక్యుమెంట్ సైన్ చేయడానికి మొబైల్ బ్యాటరీలో 0.01% కన్నా తక్కువ మాత్రమే ఖర్చవుతుంది."
                }
            ]
        },
        {
            "cat_title": "Category 3: Legal, CCA India & Cryptographic Compliance (చట్టబద్ధత & నిబంధనలు)",
            "color": "6B21A8",
            "questions": [
                {
                    "q_num": "Q8",
                    "q_eng": "Is this legally valid in Indian Courts under the IT Act 2000?",
                    "q_tel": "భారత ఐటీ చట్టం 2000 ప్రకారం ఈ మొబైల్ సంతకం కోర్టులలో చెల్లుబాటు అవుతుందా?",
                    "sc_eng": "\"100% legally valid under Section 3 & 3A of the IT Act 2000 and CCA India rules.\"",
                    "sc_tel": "\"ఐటీ చట్టం సెక్షన్ 3 & 3A ప్రకారం భారతదేశంలోని అన్ని కోర్టులలో 100% చెల్లుబాటు అవుతుంది.\"",
                    "ans_eng": "100% Legally Valid. Fully adheres to Section 3 & Section 3A of the Indian Information Technology Act 2000. Uses licensed Certifying Authorities (eMudhra, Capricorn, VSign, NSDL) under the Controller of Certifying Authorities (CCA India).",
                    "ans_tel": "100% చట్టబద్ధమైనది. భారత ఐటీ చట్టం 2000 లోని సెక్షన్ 3 మరియు 3A నిబంధనలకు సంపూర్ణంగా లోబడి ఉంటుంది. లైసెన్స్ పొందిన eMudhra, Capricorn, VSign సర్టిఫికెట్లతో కోర్టులలో చెల్లుబాటు అవుతుంది."
                },
                {
                    "q_num": "Q9",
                    "q_eng": "Why does Adobe Acrobat Reader display a Green Checkmark for our signed files?",
                    "q_tel": "అడోబ్ రీడర్‌లో మన సంతకం ఫైళ్లకు ఆకుపచ్చ టిక్ మార్క్ (Green Tick) ఎందుకు వస్తుంది?",
                    "sc_eng": "\"PAdES-LTV (ETSI EN 319 142) + RFC 3161 TSA guarantees official Green Tick.\"",
                    "sc_tel": "\"PAdES-LTV మరియు టైమ్‌స్టాంప్ ఉండటం వల్ల అడోబ్‌లో అసలైన గ్రీన్ టిక్ మార్క్ వస్తుంది.\"",
                    "ans_eng": "Because SecureSign packages standard PAdES-LTV (ETSI EN 319 142) containers with embedded RFC 3161 TSA timestamps and DSS revocation chains. Adobe Acrobat parses the certificate trust tree and confirms 'Signature is Valid'.",
                    "ans_tel": "ఎందుకంటే సెక్యూర్‌సైన్ అంతర్జాతీయ PAdES-LTV ప్రమాణాలతో పాటు RFC 3161 టైమ్‌స్టాంప్‌ను ఫైల్‌లో బంధిస్తుంది. దీనివల్ల అడోబ్ రీడర్ అధికారిక గ్రీన్ టిక్ మార్క్ చూపిస్తుంది."
                },
                {
                    "q_num": "Q10",
                    "q_eng": "What happens if an officer's signing certificate has expired or been revoked?",
                    "q_tel": "అధికారి సర్టిఫికెట్ గడువు ముగిసినా లేదా రద్దయినా (Revoked) సిస్టమ్ ఏం చేస్తుంది?",
                    "sc_eng": "\"Live OCSP and CRL revocation checks automatically block invalid certificates.\"",
                    "sc_tel": "\"ఆన్‌లైన్ OCSP ద్వారా రద్దయిన సర్టిఫికెట్లను సిస్టమ్ వెంటనే బ్లాక్ చేస్తుంది.\"",
                    "ans_eng": "During PAdES assembly, the backend queries live OCSP (Online Certificate Status Protocol) and CRL responders. If revoked or expired, signing is immediately blocked and logged into the audit trail.",
                    "ans_tel": "సైనింగ్ సమయంలో ఆన్‌లైన్ OCSP మరియు CRL రెస్పాండర్స్ ద్వారా సర్టిఫికెట్ స్థితిని పరిశీలిస్తుంది. సర్టిఫికెట్ రద్దయి ఉంటే సంతకం చేయడాన్ని వెంటనే నిలిపివేస్తుంది."
                }
            ]
        },
        {
            "cat_title": "Category 4: AP State e-Governance Integration & Scalability (ఏపీ ప్రభుత్వం & పైలట్)",
            "color": "065F46",
            "questions": [
                {
                    "q_num": "Q11",
                    "q_eng": "How does SecureSign integrate with AP e-Office and CFMS?",
                    "q_tel": "ఆంధ్రప్రదేశ్ ఈ-ఆఫీస్ మరియు CFMS వ్యవస్థలతో దీనిని ఎలా అనుసంధానిస్తారు?",
                    "sc_eng": "\"Plug-and-play Android App Intent, REST API, or embedded Android SDK (.AAR).\"",
                    "sc_tel": "\"ఆండ్రాయిడ్ యాప్ ఇంటెంట్, REST API లేదా SDK ద్వారా సులభంగా అనుసంధానించవచ్చు.\"",
                    "ans_eng": "We provide three seamless integration modes:\n1. Android App Intent / Deep Link: AP e-Office mobile app invokes SecureSign via intent and receives signed PDF callback in <2s.\n2. REST API: Direct microservice integration hosted on AP State Data Center.\n3. Embedded Android SDK (.AAR): Library embedded directly inside AP e-Office.",
                    "ans_tel": "మేము 3 సులభమైన పద్ధతులను అందిస్తున్నాము:\n1. ఆండ్రాయిడ్ యాప్ ఇంటెంట్: ఏపీ ఈ-ఆఫీస్ యాప్ నుండి సెక్యూర్‌సైన్ ఓపెన్ అయి 2 సెకన్లలో సైన్డ్ PDF తిరిగి ఇస్తుంది.\n2. REST API: స్టేట్ డేటా సెంటర్ (APSDC) లో సర్వర్ ఇంటిగ్రేషన్.\n3. ఎంబెడెడ్ SDK (.AAR): ఈ-ఆఫీస్ యాప్‌లోనే నేరుగా లైబ్రరీని చేర్చవచ్చు."
                },
                {
                    "q_num": "Q12",
                    "q_eng": "Can an officer sign files in remote rural villages with zero internet connectivity?",
                    "q_tel": "గ్రామాలలో ఇంటర్నెట్ లేదా నెట్‌వర్క్ లేకపోయినా సంతకం చేయవచ్చా?",
                    "sc_eng": "\"100% Offline Signing on device + auto-sync when network returns.\"",
                    "sc_tel": "\"ఇంటర్నెట్ లేకుండా 100% ఆఫ్‌లైన్ లోనే సంతకం పూర్తవుతుంది; నెట్ రాగానే సింక్ అవుతుంది.\"",
                    "ans_eng": "YES. The cryptographic handshake between mobile and Type-C DSC dongle is 100% offline over physical USB CCID lines. The file is signed locally and automatically synchronizes with e-Office once connectivity resumes.",
                    "ans_tel": "అవును! మొబైల్ మరియు డోంగిల్ మధ్య కమ్యూనికేషన్ 100% ఆఫ్‌లైన్‌లో USB ద్వారా జరుగుతుంది. ఇంటర్నెట్ లేకపోయినా ఫైల్ సంతకం పూర్తవుతుంది; నెట్ రాగానే సర్వర్‌కి ఆటో-సింక్ అవుతుంది."
                },
                {
                    "q_num": "Q13",
                    "q_eng": "What is the proposed deployment roadmap for the Government of Andhra Pradesh?",
                    "q_tel": "ఆంధ్రప్రదేశ్ ప్రభుత్వానికి మీరు ప్రతిపాదించే పైలట్ మరియు విస్తరణ ప్రణాళిక ఏమిటి?",
                    "sc_eng": "\"14-day Secretariat Pilot -> 30-day 26 District Collectorates -> Statewide rollout.\"",
                    "sc_tel": "\"14 రోజుల్లో సెక్రటేరియట్ పైలట్ -> 30 రోజుల్లో 26 జిల్లా కలెక్టరేట్లకు విస్తరణ.\"",
                    "ans_eng": "• Phase 1 (Days 1–14): Immediate Pilot with 50 Principal Secretaries in AP Secretariat.\n• Phase 2 (Days 15–30): Rollout to 26 District Collectorates & Joint Collectors.\n• Phase 3 (Day 45+): Statewide rollout covering 50,000+ government officers across all departments.",
                    "ans_tel": "• మొదటి దశ (14 రోజులు): ఏపీ సచివాలయంలో 50 మంది ముఖ్య కార్యదర్శులతో తక్షణ పైలట్.\n• రెండవ దశ (30 రోజులు): రాష్ట్రంలోని 26 జిల్లాల కలెక్టరేట్లకు విస్తరణ.\n• మూడవ దశ (45+ రోజులు): రాష్ట్రవ్యాప్తంగా 50,000+ మంది ప్రభుత్వ అధికారులకు పూర్తిస్థాయి అమలు."
                }
            ]
        }
    ]
    
    for cat in categories:
        p_ch = doc.add_paragraph()
        p_ch.paragraph_format.space_before = Pt(8)
        p_ch.paragraph_format.space_after = Pt(4)
        r = p_ch.add_run(cat["cat_title"])
        r.font.name = "Nirmala UI"
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(15, 23, 42)
        
        for q in cat["questions"]:
            # Card Table for Each Question
            t_q = doc.add_table(rows=3, cols=1)
            t_q.alignment = WD_TABLE_ALIGNMENT.CENTER
            
            # Row 0: Question Title (Bilingual)
            c0 = t_q.cell(0, 0)
            set_cell_background(c0, "1E293B") # Slate 800
            set_cell_margins(c0, top=60, bottom=60, left=120, right=120)
            p0 = c0.paragraphs[0]
            r0 = p0.add_run(f"[{q['q_num']}] 🇬🇧 {q['q_eng']}\n     🇮🇳 {q['q_tel']}")
            r0.font.name = "Nirmala UI"
            r0.font.bold = True
            r0.font.size = Pt(9)
            r0.font.color.rgb = RGBColor(255, 255, 255)
            
            # Row 1: Golden 1-Line Shortcuts Box (Amber Highlight)
            c1 = t_q.cell(1, 0)
            set_cell_background(c1, "FEF3C7") # Amber 100
            set_cell_margins(c1, top=60, bottom=60, left=120, right=120)
            p1 = c1.paragraphs[0]
            r1_title = p1.add_run("⚡ 1-LINE INSTANT SHORTCUTS / 1-లైన్ సూటి సమాధానం:\n")
            r1_title.font.name = "Nirmala UI"
            r1_title.font.bold = True
            r1_title.font.size = Pt(8.5)
            r1_title.font.color.rgb = RGBColor(146, 64, 14)
            
            r1_eng = p1.add_run(f"• 🇬🇧 English: {q['sc_eng']}\n")
            r1_eng.font.name = "Segoe UI"
            r1_eng.font.bold = True
            r1_eng.font.size = Pt(8.5)
            r1_eng.font.color.rgb = RGBColor(30, 64, 175)
            
            r1_tel = p1.add_run(f"• 🇮🇳 తెలుగు: {q['sc_tel']}")
            r1_tel.font.name = "Nirmala UI"
            r1_tel.font.bold = True
            r1_tel.font.size = Pt(8.5)
            r1_tel.font.color.rgb = RGBColor(6, 95, 70)
            
            # Row 2: Detailed Technical Answers (Bilingual Parallel)
            c2 = t_q.cell(2, 0)
            set_cell_background(c2, "F8FAFC") # Slate 50
            set_cell_margins(c2, top=80, bottom=80, left=120, right=120)
            p2 = c2.paragraphs[0]
            
            r2_eng_t = p2.add_run("🇬🇧 Detailed Technical Defense:\n")
            r2_eng_t.font.name = "Segoe UI"
            r2_eng_t.font.bold = True
            r2_eng_t.font.size = Pt(8.5)
            r2_eng_t.font.color.rgb = RGBColor(15, 23, 42)
            
            r2_eng = p2.add_run(f"{q['ans_eng']}\n\n")
            r2_eng.font.name = "Segoe UI"
            r2_eng.font.size = Pt(8.5)
            r2_eng.font.color.rgb = RGBColor(51, 65, 85)
            
            r2_tel_t = p2.add_run("🇮🇳 తెలుగు పూర్తి వివరణ:\n")
            r2_tel_t.font.name = "Nirmala UI"
            r2_tel_t.font.bold = True
            r2_tel_t.font.size = Pt(8.5)
            r2_tel_t.font.color.rgb = RGBColor(6, 95, 70)
            
            r2_tel = p2.add_run(f"{q['ans_tel']}")
            r2_tel.font.name = "Nirmala UI"
            r2_tel.font.size = Pt(8.5)
            r2_tel.font.color.rgb = RGBColor(15, 23, 42)
            
            doc.add_paragraph().paragraph_format.space_after = Pt(3)
            
    doc.add_page_break()
    
    # 4-STEP LIVE DEMO & ACTIVITY DIAGRAM
    p_demo_title = doc.add_paragraph()
    r = p_demo_title.add_run("4-STEP LIVE DEMO FORMULA & SYSTEM STATE MACHINE\nలైవ్ డెమో 4 దశల సూత్రం & యాక్టివిటీ ఫ్లోచార్ట్ (English & తెలుగు)")
    r.font.name = "Nirmala UI"
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    # 4 Demo Cards Table
    t_d4 = doc.add_table(rows=1, cols=4)
    t_d4.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    demo_steps = [
        ("1. PLUG (కనెక్ట్)", "Plug Type-C Dongle into Android phone.", "మొబైల్‌కు టైప్-సి డోంగిల్ కనెక్ట్ చేయండి."),
        ("2. DETECT (గుర్తింపు)", "App detects token & reads eMudhra cert.", "యాప్ సర్టిఫికెట్ వివరాలు గుర్తిస్తుంది."),
        ("3. SIGN (సంతకం)", "Enter PIN -> Signs PDF in under 2s.", "పిన్ ఎంటర్ చేసి 2 సెకన్లలో సైన్ చేయండి."),
        ("4. VERIFY (ధృవీకరణ)", "Open in Adobe -> Shows Green Tick.", "అడోబ్‌లో గ్రీన్ టిక్ మార్క్ చూపించండి.")
    ]
    
    for i, (title, eng, tel) in enumerate(demo_steps):
        cell = t_d4.cell(0, i)
        set_cell_background(cell, "FEF3C7")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        r1 = p.add_run(f"{title}\n")
        r1.font.name = "Nirmala UI"
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = RGBColor(146, 64, 14)
        
        r2 = p.add_run(f"{eng}\n")
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(8)
        r2.font.color.rgb = RGBColor(15, 23, 42)
        
        r3 = p.add_run(f"{tel}")
        r3.font.name = "Nirmala UI"
        r3.font.bold = True
        r3.font.size = Pt(8)
        r3.font.color.rgb = RGBColor(6, 95, 70)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Activity Diagram Image
    act_img_path = 'uploads/SecureSign_Activity_Diagram.png'
    if not os.path.exists(act_img_path) and os.path.exists('SecureSign_Activity_Diagram.png'):
        act_img_path = 'SecureSign_Activity_Diagram.png'
        
    if os.path.exists(act_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(act_img_path, width=Inches(6.8))
        
    # Emergency Plan Table
    t_em = doc.add_table(rows=3, cols=3)
    t_em.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    em_headers = ["Scenario / సమస్య", "Action / చేయవలసిన పని", "What to Say / చెప్పవలసిన సమాధానం"]
    for i, h in enumerate(em_headers):
        cell = t_em.cell(0, i)
        set_cell_background(cell, "B91C1C") # Crimson
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Nirmala UI"
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    em_rows = [
        (
            "Screen share lags on Meet\n(స్క్రీన్ షేర్ స్లో అయితే)",
            "Play backup video SecureSign_Demonstration_Video.mp4 or show test_signed_output.pdf in Adobe Reader.",
            "\"While the screen mirror reconnects, let me show you the verified signed PDF in Adobe Acrobat Reader.\"\n(స్క్రీన్ కనెక్ట్ అయ్యేలోపు అడోబ్‌లో వెరిఫై అయిన ఫైల్ చూపిస్తున్నాను.)"
        ),
        (
            "Dongle not detected on first plug\n(డోంగిల్ వెంటనే కనెక్ట్ కాకపోతే)",
            "Unplug and replug firmly, accept the Android USB prompt 'Always open SecureSign'.",
            "\"Android is establishing the secure CCID connection through the hardware USB bus.\"\n(ఆండ్రాయిడ్ సిస్టమ్ హార్డ్‌వేర్ USB కనెక్షన్‌ను ప్రారంభిస్తోంది.)"
        )
    ]
    
    for row_idx, (sc, ac, ws) in enumerate(em_rows, start=1):
        row = t_em.rows[row_idx]
        for col_idx, text in enumerate([sc, ac, ws]):
            cell = row.cells[col_idx]
            set_cell_background(cell, "FEF2F2" if row_idx % 2 != 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Nirmala UI"
            r.font.size = Pt(8)
            
    # Save docx
    docx_path = os.path.abspath('SecureSign_Complete_Jury_QA_and_Visual_Workflow_Timeline.docx')
    pdf_out = os.path.abspath('SecureSign_Complete_Jury_QA_and_Visual_Workflow_Timeline.pdf')
    doc.save(docx_path)
    print("Saved DOCX:", docx_path)
    
    # Convert to PDF via Word
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    wb = word.Documents.Open(docx_path)
    wb.SaveAs(pdf_out, FileFormat=17) # 17 = wdFormatPDF
    wb.Close()
    word.Quit()
    print("Converted to PDF via Word:", pdf_out)
    
    # Copy to uploads folder
    shutil.copy(docx_path, os.path.join('uploads', os.path.basename(docx_path)))
    shutil.copy(pdf_out, os.path.join('uploads', os.path.basename(pdf_out)))
    print("Successfully published to uploads folder!")

if __name__ == '__main__':
    create_document()
