import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = docx.Document()

# Set standard page margins
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Helper function to set cell background color
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

# Helper function to style headings
def add_custom_heading(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(11, 19, 43)  # Deep Navy
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0, 122, 255)  # Electric Blue
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(16, 185, 129)  # Emerald Green
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
    return p

def add_code_box(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.8)
    set_cell_background(cell, '0B132B')
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(56, 189, 248)  # Sky Blue Terminal Text
    doc.add_paragraph('')

# ── Title Page / Header ──
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_p.add_run('SECURESIGN: SYSTEM ARCHITECTURE & WORKFLOW SPECIFICATION\n')
title_run.bold = True
title_run.font.size = Pt(20)
title_run.font.color.rgb = RGBColor(11, 19, 43)

sub_run = title_p.add_run('Comprehensive Visual Architecture, Sequence Flows, Protocol Stacks & Security Models\n')
sub_run.font.size = Pt(12)
sub_run.font.italic = True
sub_run.font.color.rgb = RGBColor(70, 80, 95)

meta_run = title_p.add_run('Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026\nLead Contact: pmahi7801@gmail.com | Live API: https://hackthonapp-production.up.railway.app\n')
meta_run.font.size = Pt(9.5)
meta_run.font.color.rgb = RGBColor(0, 122, 255)

doc.add_paragraph('─' * 75)

# ── Section 1: High-Level Architecture Diagram ──
add_custom_heading(doc, '1. High-Level Multi-Tier System Architecture', level=1)
p = doc.add_paragraph('The diagram below illustrates the 5 distinct architectural tiers of SecureSign, showing the physical boundary between the mobile device, native Android kernel, cryptographic hardware chip, and cloud services.')

arch_diagram = """
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TIER 1: MOBILE CLIENT (UI / UX)                            │
│  React Navigation • Document Picker • PIN Entry Screen • PAdES Viewer • Session Manager    │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │ React Native NativeModules Bridge (JNI)
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                          TIER 2: NATIVE ANDROID DRIVER & PROTOCOL STACK                     │
│  • android.hardware.usb.UsbManager (Host Mode) • UsbDeviceConnection (Bulk IN/OUT 0x82/0x02)│
│  • CcidTransport.kt (USB CCID Class 0x0B Engine)  • P11Wrapper.kt (PKCS#11 APDU Translator) │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │ Physical USB Type-C OTG Interface
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                     TIER 3: HARDWARE DSC CRYPTOGRAPHIC COPROCESSOR (TOKEN)                  │
│  • FIPS 140-2 Level 3 / CC EAL 5+ Secure Element (ePass2003 / Watchdata / Gemalto / mToken) │
│  • On-Chip Key Storage (RSA-2048 Private Key) ── NEVER LEAVES TOKEN (CCA Rule 1)            │
│  • Hardware PIN Verification Engine (VERIFY APDU 0x00 0x20) ── Zero RAM Cache (CCA Rule 2) │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │ Cryptographic Signature Output (PKCS#1v1.5)
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                        TIER 4: CLOUD PAdES ASSEMBLY & TIMESTAMP AUTHORITY                   │
│  • Express.js & Node.js Crypto Engine • RFC 3161 Trusted Time Stamping Authority (TSA)      │
│  • PDF-Lib Engine: Injects Visible CCA Digital Seal • ETSI TS 102 778 PAdES-LTV Container   │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │ Validated PAdES Stream
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                             TIER 5: VALIDATION & AUDIT VERIFICATION                         │
│  • Adobe Acrobat Reader (PAdES Validated) • Section 3A IT Act 2000 Legal Validity           │
│  • Cryptographic Audit Trail (Supabase / Postgres Store) • Railway Production Host          │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
"""
add_code_box(doc, arch_diagram)

# ── Section 2: End-to-End Workflow Sequence Diagram ──
add_custom_heading(doc, '2. End-to-End Cryptographic Sequence Flow', level=1)
p = doc.add_paragraph('This sequence diagram depicts the chronological message exchange from initial USB dongle insertion to final Adobe Acrobat verification.')

seq_diagram = """
Officer (User)      Android App (RN)       Native CCID (Kotlin)    DSC Dongle (Token)    Backend & TSA (Cloud)
     │                     │                        │                       │                      │
     │── 1. Insert Dongle ─┼───────────────────────►│                       │                      │
     │                     │                        │── 2. Claim CCID USB ─►│                      │
     │                     │◄── Token Connected ────│                       │                      │
     │                     │                        │                       │                      │
     │── 3. Pick PDF ─────►│                        │                       │                      │
     │                     │── 4. SHA-256 Hash ────►│                       │                      │
     │                     │   (e3b0c44298fc...)    │                       │                      │
     │                     │                        │                       │                      │
     │── 5. Enter PIN ────►│                        │                       │                      │
     │                     │── 6. VERIFY APDU ─────►│── 7. Check On-Chip ──►│                      │
     │                     │                        │◄── 90 00 (Success) ───│                      │
     │                     │                        │                       │                      │
     │                     │── 8. PSO:SIGN APDU ───►│── 9. RSA-2048 Sign ──►│                      │
     │                     │                        │◄── Signature Blob ────│                      │
     │                     │◄── Return Signature ───│                       │                      │
     │                     │                                                │                      │
     │                     │── 10. Assemble PAdES + Request TSA ──────────────────────────────────►│
     │                     │                                                                       │── 11. RFC 3161 TSA
     │                     │                                                                       │── 12. Stamp Seal Box
     │                     │◄── 13. Download & Open Signed PDF Stream ─────────────────────────────│
     │                     │                                                                       │
     │── 14. View in Adobe Acrobat Reader ────────────────────────────────────────────────────────►│
     │   (✅ "Signed & all signatures are valid • CCA Class-3 Verified • IT Act 2000 Sec 3A")       │
"""
add_code_box(doc, seq_diagram)

# ── Section 3: ISO 7816-4 APDU Protocol Stack Table ──
add_custom_heading(doc, '3. ISO 7816-4 Smart Card APDU Protocol Stack', level=1)
p = doc.add_paragraph('SecureSign implements the full ISO/IEC 7816-4 Command-Response APDU structure across USB bulk endpoints:')

apdu_table = doc.add_table(rows=1, cols=4)
apdu_table.alignment = WD_TABLE_ALIGNMENT.CENTER
apdu_table.autofit = False

hdr = apdu_table.rows[0].cells
hdr[0].width = Inches(1.8)
hdr[1].width = Inches(1.5)
hdr[2].width = Inches(2.3)
hdr[3].width = Inches(1.2)
hdr[0].text = 'APDU Command'
hdr[1].text = 'Hex Header (CLA INS P1 P2)'
hdr[2].text = 'Payload / Data Field'
hdr[3].text = 'Expected SW'

for c in hdr:
    set_cell_background(c, '0B132B')
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

apdu_rows = [
    ('SELECT MF / Applet', '00 A4 04 00', 'AID: A0 00 00 00 63 50 4B 43 53 2D 31 35', '90 00'),
    ('VERIFY PIN', '00 20 00 81', 'User PIN (ASCII Encoded, Zeroized after execution)', '90 00 / 63 CX'),
    ('GET CERTIFICATE', '00 CB 3F FF', 'Tag: 70 (X.509 Certificate Retrieval)', '90 00 / 61 XX'),
    ('PSO: COMPUTE SIGNATURE', '00 2A 9E 9A', 'DigestInfo Header + 32-byte SHA-256 Document Hash', '90 00'),
    ('GET RESPONSE', '00 C0 00 00', 'Le: Variable (Fetches remaining signature bytes)', '90 00')
]

for cmd, hex_hdr, payload, sw in apdu_rows:
    row = apdu_table.add_row().cells
    row[0].width = Inches(1.8)
    row[1].width = Inches(1.5)
    row[2].width = Inches(2.3)
    row[3].width = Inches(1.2)
    
    row[0].text = cmd
    row[1].text = hex_hdr
    row[2].text = payload
    row[3].text = sw
    
    set_cell_background(row[0], 'F0F4F8')
    set_cell_background(row[1], 'FFFFFF')
    set_cell_background(row[2], 'FFFFFF')
    set_cell_background(row[3], 'F0Fdf4')
    
    for c in row:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)

doc.add_paragraph('')

# ── Section 4: Security Architecture & CCA Rules ──
add_custom_heading(doc, '4. Security Architecture & CCA India Rule Enforcement', level=1)

cca_table = doc.add_table(rows=1, cols=3)
cca_table.alignment = WD_TABLE_ALIGNMENT.CENTER
cca_table.autofit = False

chdr = cca_table.rows[0].cells
chdr[0].width = Inches(1.5)
chdr[1].width = Inches(2.5)
chdr[2].width = Inches(2.8)
chdr[0].text = 'CCA Mandate'
chdr[1].text = 'Security Vulnerability Prevented'
chdr[2].text = 'SecureSign Technical Implementation'

for c in chdr:
    set_cell_background(c, '0B132B')
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

cca_rows = [
    ('Rule 1: Private Key Isolation', 'Key theft via malware or memory dumps', 'Private key is permanently trapped inside hardware crypto-coprocessor (FIPS 140-2 L3).'),
    ('Rule 2: Token PIN Verification', 'PIN interception or man-in-the-middle', 'PIN is verified on-chip via VERIFY APDU. RAM holding PIN is overwritten with 0x00 immediately.'),
    ('Rule 3: Signature Standard', 'Document repudiation or date tampering', 'Generates PAdES-LTV containers with embedded RFC 3161 Time Stamping Authority (TSA) tokens.'),
    ('Rule 4: Hardware Locking', 'Brute-force PIN guessing attacks', 'Hardware enforces max 3 retry attempts. Dongle locks at hardware level upon 3rd failure.'),
    ('Rule 5: Audit Logging', 'Audit tampering or repudiation', 'Immutable audit logs with signer ID, SHA-256 hash, IP address, and timestamp.')
]

for rule, vuln, impl in cca_rows:
    row = cca_table.add_row().cells
    row[0].width = Inches(1.5)
    row[1].width = Inches(2.5)
    row[2].width = Inches(2.8)
    
    row[0].text = rule
    row[1].text = vuln
    row[2].text = impl
    
    set_cell_background(row[0], 'F0F4F8')
    set_cell_background(row[1], 'FFFFFF')
    set_cell_background(row[2], 'FFFFFF')
    
    for c in row:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)

doc.add_paragraph('')

# ── Section 5: Summary & Links ──
add_custom_heading(doc, '5. Verification Links & Source Code References', level=1)

p = doc.add_paragraph()
p.add_run('• Production REST API: ').bold = True
p.add_run('https://hackthonapp-production.up.railway.app\n')
p.add_run('• GitHub Source Code: ').bold = True
p.add_run('https://github.com/mahankalikornepati2-netizen/hackthonapp\n')
p.add_run('• Compiled APK Build: ').bold = True
p.add_run('https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c\n')
p.add_run('• Official Google Submission Form: ').bold = True
p.add_run('https://forms.gle/TJDYkF6feKFrywsd7\n')

os.makedirs('uploads', exist_ok=True)
out1 = 'uploads/SecureSign_Architecture_and_Workflow_Diagrams.docx'
out2 = 'SecureSign_Architecture_and_Workflow_Diagrams.docx'

doc.save(out1)
doc.save(out2)

print('Successfully generated Architecture & Workflow Word Document at:')
print('1.', out1)
print('2.', out2)
