import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

os.makedirs('uploads', exist_ok=True)
doc = docx.Document()

# Page Margins
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

# Helper Functions
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(11, 19, 43) # Deep Navy
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(37, 99, 235) # Royal Blue
    return p

def add_callout(doc, title, text, bg_hex='F0F9FF', border_hex='0284C7'):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.9)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>\n'
                        f'  <w:top w:val="none"/>\n'
                        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_hex}"/>\n'
                        f'  <w:bottom w:val="none"/>\n'
                        f'  <w:right w:val="none"/>\n'
                        f'</w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    r_t = p.add_run(title + '\n')
    r_t.bold = True
    r_t.font.size = Pt(11)
    r_t.font.color.rgb = RGBColor(11, 19, 43)
    
    r_b = p.add_run(text)
    r_b.font.size = Pt(9.5)
    r_b.font.color.rgb = RGBColor(51, 65, 85)
    doc.add_paragraph('')

# ── Title & Executive Header ──
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_p.add_run('SECURESIGN: TECHNICAL ARCHITECTURE & TECHNOLOGY DOSSIER\n')
title_run.bold = True
title_run.font.size = Pt(20)
title_run.font.color.rgb = RGBColor(11, 19, 43)

sub_run = title_p.add_run('Type-C DSC Mobile Digital Signing Solution • Statutory Compliance & Protocol Specifications\n')
sub_run.font.size = Pt(11.5)
sub_run.font.italic = True
sub_run.font.color.rgb = RGBColor(71, 85, 105)

meta_run = title_p.add_run('Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026\nLead Contact: pmahi7801@gmail.com | Production API: https://hackthonapp-production.up.railway.app\n')
meta_run.font.size = Pt(9.5)
meta_run.font.color.rgb = RGBColor(37, 99, 235)

doc.add_paragraph('─' * 75)

# Executive Callout
add_callout(
    doc,
    '🏆 EXECUTIVE SUMMARY & VALUE PROPOSITION',
    'SecureSign is a mobile-first digital signature solution engineered to enable seamless, hardware-level Class-3 DSC signing directly on Android smartphones via USB Type-C OTG without requiring desktop PCs, Java applets, or third-party middleware. The solution is 100% compliant with CCA India guidelines and Section 3A of the Indian Information Technology Act 2000.'
)

# ── Section 1: Multi-Tier System Architecture ──
add_heading_1(doc, '1. Multi-Tier System Architecture')
doc.add_paragraph('SecureSign is architected into 5 modular, loosely coupled tiers ensuring strict physical separation between user interface, native hardware driver, cryptographic coprocessor, and cloud timestamping services.')

arch_table = doc.add_table(rows=1, cols=3)
arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
arch_table.autofit = False

ahdr = arch_table.rows[0].cells
ahdr[0].width = Inches(1.8)
ahdr[1].width = Inches(2.3)
ahdr[2].width = Inches(2.8)
ahdr[0].text = 'Architecture Tier'
ahdr[1].text = 'Technologies & Protocols'
ahdr[2].text = 'Core Responsibilities & Guarantees'

for c in ahdr:
    set_cell_background(c, '0B132B')
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(255, 255, 255)

arch_rows = [
    ('Tier 1: Mobile UI/UX', 'React Native 0.74+, TypeScript, Expo EAS Build', 'Intuitive signing interface, native PDF file picker, secure PIN entry, 1-tap download & share with zero OTP delays.'),
    ('Tier 2: Native USB Driver', 'Kotlin 1.9+, android.hardware.usb, JNI Bridge', 'Direct CCID driver claiming USB interface 0, managing Bulk IN/OUT (0x82/0x02) endpoints with 5000ms watchdog.'),
    ('Tier 3: Hardware Token', 'ISO 7816-4 APDU, PKCS#11, FIPS 140-2 Level 3', 'On-chip RSA-2048 private key signing, on-chip PIN verification, hardware brute-force defense (3 retries max).'),
    ('Tier 4: Cloud PAdES Engine', 'Node.js v20 LTS, Express, pdf-lib, RFC 3161 TSA', 'Constructs ETSI TS 102 778 (PAdES-LTV) containers, injects trusted X.509 timestamp, stamps visible CCA seal.'),
    ('Tier 5: Legal Verification', 'Adobe Acrobat Reader, IT Act 2000 Section 3A', 'Verifies signature against national CCA Trust Store; displays Green Verification Ribbon worldwide.')
]

for tier, tech, resp in arch_rows:
    row = arch_table.add_row().cells
    row[0].width = Inches(1.8)
    row[1].width = Inches(2.3)
    row[2].width = Inches(2.8)
    row[0].text = tier
    row[1].text = tech
    row[2].text = resp
    
    set_cell_background(row[0], 'F8FAFC')
    set_cell_background(row[1], 'FFFFFF')
    set_cell_background(row[2], 'FFFFFF')
    set_cell_margins(row[0], top=60, bottom=60, left=100, right=100)
    set_cell_margins(row[1], top=60, bottom=60, left=100, right=100)
    set_cell_margins(row[2], top=60, bottom=60, left=100, right=100)
    
    for c in row:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)

doc.add_paragraph('')

# ── Section 2: Visual Workflow & Activity Diagram ──
add_heading_1(doc, '2. End-to-End Visual Workflow & Activity Architecture')
doc.add_paragraph('The diagram below depicts the end-to-end cryptographic lifecycle from document selection to final Adobe Acrobat verification:')

img_path = 'uploads/SecureSign_Executive_Workflow_Diagram.png'
if os.path.exists(img_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(img_path, width=Inches(6.9))

doc.add_paragraph('')

# ── Section 3: ISO 7816-4 APDU Protocol Specification ──
add_heading_1(doc, '3. Smart Card ISO 7816-4 APDU Protocol Specification')
doc.add_paragraph('The custom Kotlin CCID driver (CcidTransport.kt) directly constructs and exchanges ISO/IEC 7816-4 Command-Response APDUs across the USB bulk endpoints:')

apdu_table = doc.add_table(rows=1, cols=4)
apdu_table.alignment = WD_TABLE_ALIGNMENT.CENTER
apdu_table.autofit = False

aphdr = apdu_table.rows[0].cells
aphdr[0].width = Inches(1.8)
aphdr[1].width = Inches(1.5)
aphdr[2].width = Inches(2.4)
aphdr[3].width = Inches(1.2)
aphdr[0].text = 'APDU Command'
aphdr[1].text = 'Hex (CLA INS P1 P2)'
aphdr[2].text = 'Payload / Data Field'
aphdr[3].text = 'Status Word'

for c in aphdr:
    set_cell_background(c, '0B132B')
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(255, 255, 255)

apdu_rows = [
    ('SELECT MF / Applet', '00 A4 04 00', 'AID: A0 00 00 00 63 50 4B 43 53 2D 31 35', '90 00'),
    ('VERIFY PIN', '00 20 00 81', 'User PIN (ASCII, Zeroized immediately in RAM)', '90 00 / 63 CX'),
    ('GET CERTIFICATE', '00 CB 3F FF', 'Tag: 70 (X.509 Public Certificate Data)', '90 00 / 61 XX'),
    ('PSO: COMPUTE SIGNATURE', '00 2A 9E 9A', 'DigestInfo Header + 32-byte SHA-256 Hash', '90 00'),
    ('GET RESPONSE', '00 C0 00 00', 'Le: Variable (Fetches remaining signature bytes)', '90 00')
]

for cmd, hex_hdr, payload, sw in apdu_rows:
    row = apdu_table.add_row().cells
    row[0].width = Inches(1.8)
    row[1].width = Inches(1.5)
    row[2].width = Inches(2.4)
    row[3].width = Inches(1.2)
    row[0].text = cmd
    row[1].text = hex_hdr
    row[2].text = payload
    row[3].text = sw
    
    set_cell_background(row[0], 'F8FAFC')
    set_cell_background(row[1], 'FFFFFF')
    set_cell_background(row[2], 'FFFFFF')
    set_cell_background(row[3], 'F0FDF4')
    set_cell_margins(row[0], top=60, bottom=60, left=100, right=100)
    set_cell_margins(row[1], top=60, bottom=60, left=100, right=100)
    set_cell_margins(row[2], top=60, bottom=60, left=100, right=100)
    set_cell_margins(row[3], top=60, bottom=60, left=100, right=100)
    
    for c in row:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)

doc.add_paragraph('')

# ── Section 4: CCA India Statutory Compliance Matrix ──
add_heading_1(doc, '4. CCA India Regulatory Compliance Matrix')

cca_table = doc.add_table(rows=1, cols=3)
cca_table.alignment = WD_TABLE_ALIGNMENT.CENTER
cca_table.autofit = False

chdr = cca_table.rows[0].cells
chdr[0].width = Inches(1.8)
chdr[1].width = Inches(2.4)
chdr[2].width = Inches(2.7)
chdr[0].text = 'CCA Mandate'
chdr[1].text = 'Statutory Requirement'
chdr[2].text = 'SecureSign Implementation'

for c in chdr:
    set_cell_background(c, '0B132B')
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(255, 255, 255)

cca_specs = [
    ('Rule 1: Private Key Isolation', 'Private key must NEVER leave the hardware crypto chip.', 'On-chip RSA-2048 signing inside FIPS 140-2 Level 3 Secure Element. Key extraction is impossible.'),
    ('Rule 2: Token PIN Verification', 'PIN must be verified on-chip without memory caching.', 'Direct ISO 7816-4 VERIFY APDU. PIN memory is zeroized (0x00) immediately after execution.'),
    ('Rule 3: Signature Standard', 'PAdES / CAdES standard with trusted timestamping.', 'ETSI EN 319 142-1 (PAdES-LTV) with embedded RFC 3161 Time Stamping Authority (TSA) tokens.'),
    ('Rule 4: Hardware Locking', 'Enforce hardware brute-force retry limits.', 'Hardware token locks automatically after 3 consecutive wrong PIN attempts (SW1=0x63).'),
    ('Rule 5: Audit Trail', 'Maintain immutable, tamper-evident audit logs.', 'Cryptographic audit records with signer ID, SHA-256 hash, IP address, and timestamp.')
]

for r_name, r_req, r_impl in cca_specs:
    row = cca_table.add_row().cells
    row[0].width = Inches(1.8)
    row[1].width = Inches(2.4)
    row[2].width = Inches(2.7)
    row[0].text = r_name
    row[1].text = r_req
    row[2].text = r_impl
    
    set_cell_background(row[0], 'F8FAFC')
    set_cell_background(row[1], 'FFFFFF')
    set_cell_background(row[2], 'FFFFFF')
    set_cell_margins(row[0], top=60, bottom=60, left=100, right=100)
    set_cell_margins(row[1], top=60, bottom=60, left=100, right=100)
    set_cell_margins(row[2], top=60, bottom=60, left=100, right=100)
    
    for c in row:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)

doc.add_paragraph('')

# ── Section 5: Official Submission & Live Verification Links ──
add_heading_1(doc, '5. Verification Links & Source Code References')

p_links = doc.add_paragraph()
p_links.add_run('• Production REST API: ').bold = True
p_links.add_run('https://hackthonapp-production.up.railway.app\n')
p_links.add_run('• GitHub Source Code: ').bold = True
p_links.add_run('https://github.com/mahankalikornepati2-netizen/hackthonapp\n')
p_links.add_run('• Android Standalone APK (Build #4384cd86): ').bold = True
p_links.add_run('https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c\n')
p_links.add_run('• Official Google Form: ').bold = True
p_links.add_run('https://forms.gle/TJDYkF6feKFrywsd7\n')
p_links.add_run('• Lead Innovator Email: ').bold = True
p_links.add_run('pmahi7801@gmail.com\n')

out_docx1 = 'uploads/SecureSign_Technology_Details_and_Architecture_Dossier.docx'
out_docx2 = 'SecureSign_Technology_Details_and_Architecture_Dossier.docx'

doc.save(out_docx1)
doc.save(out_docx2)

print(f"Successfully generated Master Technology Dossier at:")
print(f"1. {out_docx1}")
print(f"2. {out_docx2}")
