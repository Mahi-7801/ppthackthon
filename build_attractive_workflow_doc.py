import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

doc = docx.Document()

# Set standard page margins
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

# Helper function to set cell background color
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=200, right=200):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_step_card(doc, step_num, title, icon, color_hex, badge_text, details, output_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(7.0)
    set_cell_background(cell, 'F8FAFC')
    set_cell_margins(cell, top=180, bottom=180, left=240, right=240)
    
    # Border
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>\n'
                        f'  <w:top w:val="single" w:sz="12" w:space="0" w:color="{color_hex}"/>\n'
                        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{color_hex}"/>\n'
                        f'  <w:bottom w:val="single" w:sz="12" w:space="0" w:color="{color_hex}"/>\n'
                        f'  <w:right w:val="single" w:sz="12" w:space="0" w:color="{color_hex}"/>\n'
                        f'</w:tcBorders>')
    tcPr.append(borders)
    
    # Header Paragraph
    hp = cell.paragraphs[0]
    hp.paragraph_format.space_before = Pt(2)
    hp.paragraph_format.space_after = Pt(4)
    
    r_step = hp.add_run(f"STEP {step_num}  |  {icon} {title}   ")
    r_step.bold = True
    r_step.font.size = Pt(13)
    r_step.font.color.rgb = RGBColor(11, 19, 43)
    
    r_badge = hp.add_run(f"[{badge_text}]")
    r_badge.bold = True
    r_badge.font.size = Pt(9.5)
    r_badge.font.color.rgb = RGBColor(0, 122, 255)
    
    # Details
    for line in details:
        dp = cell.add_paragraph()
        dp.paragraph_format.space_before = Pt(2)
        dp.paragraph_format.space_after = Pt(2)
        r_bullet = dp.add_run("• ")
        r_bullet.bold = True
        r_bullet.font.color.rgb = RGBColor(0, 122, 255)
        r_text = dp.add_run(line)
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
        
    # Output Banner
    op = cell.add_paragraph()
    op.paragraph_format.space_before = Pt(6)
    op.paragraph_format.space_after = Pt(2)
    r_out_label = op.add_run("➔ Output / Security Guarantee: ")
    r_out_label.bold = True
    r_out_label.font.size = Pt(9.5)
    r_out_label.font.color.rgb = RGBColor(16, 185, 129)
    
    r_out_text = op.add_run(output_text)
    r_out_text.font.size = Pt(9.5)
    r_out_text.font.color.rgb = RGBColor(15, 23, 42)
    r_out_text.bold = True

    # Arrow spacer
    if int(step_num) < 7:
        arrow_p = doc.add_paragraph()
        arrow_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        arrow_p.paragraph_format.space_before = Pt(4)
        arrow_p.paragraph_format.space_after = Pt(4)
        r_arr = arrow_p.add_run("⬇  ⬇  ⬇")
        r_arr.bold = True
        r_arr.font.size = Pt(12)
        r_arr.font.color.rgb = RGBColor(0, 122, 255)

# ── Title Page / Header ──
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_p.add_run('SECURESIGN: VISUAL WORKFLOW & ARCHITECTURE SPECIFICATION\n')
title_run.bold = True
title_run.font.size = Pt(22)
title_run.font.color.rgb = RGBColor(11, 19, 43)

sub_run = title_p.add_run('Executive-Ready End-to-End Cryptographic Process Flow for Hackathon Evaluators\n')
sub_run.font.size = Pt(13)
sub_run.font.italic = True
sub_run.font.color.rgb = RGBColor(71, 85, 105)

meta_run = title_p.add_run('Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026\nLead Contact: pmahi7801@gmail.com | Live API: https://hackthonapp-production.up.railway.app\n')
meta_run.font.size = Pt(10)
meta_run.font.color.rgb = RGBColor(0, 122, 255)

doc.add_paragraph('─' * 75)

# ── Visual Workflow Header ──
p_head = doc.add_paragraph()
p_head.paragraph_format.space_before = Pt(8)
p_head.paragraph_format.space_after = Pt(12)
r_head = p_head.add_run('7-STEP VISUAL WORKFLOW: FROM PDF PICK TO ADOBE ACROBAT VALIDATION')
r_head.bold = True
r_head.font.size = Pt(15)
r_head.font.color.rgb = RGBColor(11, 19, 43)

# ── 7 Step Cards ──
add_step_card(
    doc,
    step_num='1',
    title='Document Selection & On-Device SHA-256 Hashing',
    icon='📄',
    color_hex='007AFF',
    badge_text='MOBILE FRONTEND',
    details=[
        'User opens SecureSign on Android and taps "Pick Document to Sign (PDF)".',
        'Android DocumentPicker selects user\'s multi-page PDF (e.g. vonedigitals.com report / AP Govt Order).',
        'Native crypto engine computes mathematical SHA-256 Digest (e.g. c9c39bd020859827...).',
        'Original PDF content remains strictly on-device; unencrypted documents are never sent over public network.'
    ],
    output_text='Zero Key Leakage Architecture • 32-byte SHA-256 Digest Ready'
)

add_step_card(
    doc,
    step_num='2',
    title='USB Type-C OTG Detection & Native CCID Transport',
    icon='🔌',
    color_hex='6366F1',
    badge_text='NATIVE KOTLIN DRIVER',
    details=[
        'User plugs Type-C DSC Token (ePass2003 / Watchdata / ProxKey / Gemalto) into smartphone.',
        'Android Linux kernel detects USB Class 11 (0x0B Smart Card / CCID) and triggers USB_DEVICE_ATTACHED Intent.',
        'Custom Native Kotlin Driver (CcidTransport.kt) claims USB Interface 0 without external PC drivers.',
        'Initializes Bulk IN (0x82) & Bulk OUT (0x02) endpoints with 5000ms watchdog timer.'
    ],
    output_text='Direct Hardware CCID Channel Established via Android USB Host API'
)

add_step_card(
    doc,
    step_num='3',
    title='Hardware Token Authentication & On-Chip PIN Verification',
    icon='🔐',
    color_hex='8B5CF6',
    badge_text='CCA RULE 2 COMPLIANCE',
    details=[
        'User enters their 8-digit DSC Token PIN (e.g. 12345678) on SecureSign PIN screen.',
        'Native bridge formats ISO 7816-4 APDU command: [00 20 00 81 08 <PIN_BYTES>].',
        'PIN is verified directly inside the secure crypto coprocessor chip.',
        'Memory buffer containing PIN is zeroized (overwritten with 0x00) immediately after APDU execution.'
    ],
    output_text='Token Responds: 90 00 (Success) • Hardware Retry Limit Guard Active (Rule 4)'
)

add_step_card(
    doc,
    step_num='4',
    title='On-Chip Cryptographic Digital Signing',
    icon='⚡',
    color_hex='F59E0B',
    badge_text='CCA RULE 1 COMPLIANCE',
    details=[
        'App dispatches PSO: COMPUTE SIGNATURE APDU: [00 2A 9E 9A <DigestInfo + SHA256>].',
        'Token\'s FIPS 140-2 Level 3 / CC EAL 5+ coprocessor executes RSA-2048 signing on-chip.',
        'Token signs the hash using its burned-in Private Key (Class-3 DSC Signing Key).',
        'The Private Key NEVER leaves the physical hardware token chip under any circumstance.'
    ],
    output_text='PKCS#1v1.5 256-byte Digital Signature Blob Generated on Hardware Chip'
)

add_step_card(
    doc,
    step_num='5',
    title='RFC 3161 Trusted Time Stamping (TSA) & PAdES Assembly',
    icon='⏱️',
    color_hex='10B981',
    badge_text='CCA RULE 3 COMPLIANCE',
    details=[
        'Cloud backend receives signature blob + document hash over TLS 1.3 encrypted connection.',
        'Submits timestamp request to RFC 3161 Time Stamping Authority (TSA).',
        'TSA returns cryptographically signed X.509 timestamp token proving exact time of signing.',
        'Constructs ETSI EN 319 142-1 (PAdES-LTV) container with ByteRange dictionary locking.'
    ],
    output_text='Legally Binding PAdES-LTV Signature Container Assembled'
)

add_step_card(
    doc,
    step_num='6',
    title='Visible Government Certificate Seal Stamping',
    icon='🏛️',
    color_hex='06B6D4',
    badge_text='PDF-LIB VISUAL ENGINE',
    details=[
        'pdf-lib engine loads user\'s original multi-page PDF with 100% fidelity.',
        'Stamps official Government of AP / CCA Class-3 Blue & Green Certificate Seal Box on Page 2.',
        'Includes Signer Name, DSC Certificate Serial, RFC 3161 Timestamp, and SHA-256 Hash.',
        'Preserves all original charts, tables, text, and formatting with zero alterations.'
    ],
    output_text='Tamper-Evident Visual Certificate Seal Stamped on Original PDF'
)

add_step_card(
    doc,
    step_num='7',
    title='1-Tap Download & Adobe Acrobat Validation',
    icon='✅',
    color_hex='059669',
    badge_text='IT ACT 2000 SEC 3A VALID',
    details=[
        'User taps "📥 Download & Open Signed PDF" ➔ Opens instantly in Adobe Acrobat Reader (Zero OTP!).',
        'Adobe Acrobat verifies the signature against national CCA Trust Store.',
        'Displays Green Banner: "✅ Signed and all signatures are valid".',
        'Document carries 100% legal validity across all Andhra Pradesh Government e-Governance portals.'
    ],
    output_text='Document 100% Legally Valid & Verifiable Worldwide in Adobe Acrobat'
)

doc.add_page_break()

# ── Architectural Component Mapping Table ──
p_comp = doc.add_paragraph()
p_comp.paragraph_format.space_before = Pt(8)
p_comp.paragraph_format.space_after = Pt(10)
r_comp = p_comp.add_run('TECHNICAL COMPONENT & PROTOCOL STACK SPECIFICATION')
r_comp.bold = True
r_comp.font.size = Pt(14)
r_comp.font.color.rgb = RGBColor(11, 19, 43)

table_c = doc.add_table(rows=1, cols=3)
table_c.alignment = WD_TABLE_ALIGNMENT.CENTER
table_c.autofit = False

chdrs = table_c.rows[0].cells
chdrs[0].width = Inches(1.8)
chdrs[1].width = Inches(2.2)
chdrs[2].width = Inches(3.0)
chdrs[0].text = 'Architecture Layer'
chdrs[1].text = 'Technologies & Protocols'
chdrs[2].text = 'Core Responsibility & Features'

for c in chdrs:
    set_cell_background(c, '0B132B')
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

comp_rows = [
    ('1. Mobile Frontend Layer', 'React Native 0.74+, TypeScript, Expo EAS Build', 'Intuitive UI/UX, document picking, PIN input, 1-tap download, zero-OTP sharing.'),
    ('2. Native Android Bridge', 'Kotlin 1.9+, android.hardware.usb, JNI NativeModules', 'Direct USB Host CCID driver, USB permission handling, bulk transfer endpoint management.'),
    ('3. Hardware Crypto Layer', 'ISO 7816-4 APDU, PKCS#11, FIPS 140-2 Level 3', 'On-chip RSA-2048 signing, on-chip PIN verification, hardware brute-force defense.'),
    ('4. Cloud Security Layer', 'Node.js v20 LTS, Express, pdf-lib, RFC 3161 TSA', 'PAdES-LTV container construction, trusted timestamp injection, visible seal stamping.'),
    ('5. Audit & Compliance Layer', 'Supabase PostgreSQL 15, JWT Auth, ETSI TS 102 778', 'Tamper-evident audit logging, legal compliance under IT Act 2000 Section 3A.')
]

for l, tech, resp in comp_rows:
    row = table_c.add_row().cells
    row[0].width = Inches(1.8)
    row[1].width = Inches(2.2)
    row[2].width = Inches(3.0)
    
    row[0].text = l
    row[1].text = tech
    row[2].text = resp
    
    set_cell_background(row[0], 'F0F4F8')
    set_cell_background(row[1], 'FFFFFF')
    set_cell_background(row[2], 'FFFFFF')
    
    for c in row:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(9)

doc.add_paragraph('')

# ── Summary & Verification Links ──
p_links = doc.add_paragraph()
p_links.add_run('Official Submission & Verification Links:\n').bold = True
p_links.add_run('• Production API (Railway): https://hackthonapp-production.up.railway.app\n')
p_links.add_run('• GitHub Source Code: https://github.com/mahankalikornepati2-netizen/hackthonapp\n')
p_links.add_run('• Android APK Build #4384cd86: https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c\n')
p_links.add_run('• Official Google Form: https://forms.gle/TJDYkF6feKFrywsd7\n')

os.makedirs('uploads', exist_ok=True)
out1 = 'uploads/SecureSign_Visual_Workflow_Architecture.docx'
out2 = 'SecureSign_Visual_Workflow_Architecture.docx'

doc.save(out1)
doc.save(out2)

print('Successfully generated Visual Workflow Word Document at:')
print('1.', out1)
print('2.', out2)
