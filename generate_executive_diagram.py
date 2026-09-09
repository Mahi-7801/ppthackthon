import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

os.makedirs('uploads', exist_ok=True)

# ── 1. Create Stunning Ultra-HD Executive Activity Diagram ──
fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis('off')

# Background canvas
canvas_bg = patches.Rectangle((0, 0), 18, 12, facecolor='#F8FAFC', zorder=0)
ax.add_patch(canvas_bg)

# Phase Background Swimlane Containers
def draw_phase_container(ax, x, y, width, height, title, color_hex, tag_text):
    rect = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        facecolor='#FFFFFF', edgecolor=color_hex, linewidth=1.5, zorder=1, alpha=0.95
    )
    ax.add_patch(rect)
    
    # Header ribbon for phase
    hdr = patches.FancyBboxPatch(
        (x, y + height - 0.55), width, 0.55,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        facecolor=color_hex, edgecolor='none', zorder=2
    )
    ax.add_patch(hdr)
    ax.text(x + 0.3, y + height - 0.28, title, fontsize=10.5, fontweight='bold', color='#FFFFFF', zorder=3, va='center')
    ax.text(x + width - 0.3, y + height - 0.28, tag_text, fontsize=8.5, fontweight='bold', color='#FFFFFF', zorder=3, va='center', ha='right')

# Draw 4 Phase Containers
draw_phase_container(ax, 0.8, 6.2, 5.2, 4.4, "PHASE 1: DOCUMENT INTAKE", "#2563EB", "MOBILE DEVICE")
draw_phase_container(ax, 6.4, 6.2, 5.2, 4.4, "PHASE 2: HARDWARE CCID & PIN", "#7C3AED", "USB TYPE-C TOKEN")
draw_phase_container(ax, 12.0, 6.2, 5.2, 4.4, "PHASE 3: ON-CHIP SIGNING", "#D97706", "FIPS 140-2 L3 CHIP")
draw_phase_container(ax, 0.8, 1.2, 16.4, 4.4, "PHASE 4: CLOUD PAdES ASSEMBLY, VISIBLE SEAL & ADOBE VERIFICATION", "#059669", "LEGAL DELIVERY")

# Styled Activity Card Function
def draw_card(ax, x, y, width, height, step_num, title, subtitle, badge_color="#2563EB", fill="#FFFFFF", edge="#CBD5E1"):
    # Drop shadow
    shadow = patches.FancyBboxPatch(
        (x + 0.04, y - 0.04), width, height,
        boxstyle="round,pad=0.06,rounding_size=0.15",
        facecolor='#94A3B8', edgecolor='none', alpha=0.3, zorder=3
    )
    ax.add_patch(shadow)
    
    # Main Box
    card = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.06,rounding_size=0.15",
        facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=4
    )
    ax.add_patch(card)
    
    # Step Badge Pill
    pill = patches.FancyBboxPatch(
        (x + 0.15, y + height - 0.35), 0.7, 0.22,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=badge_color, edgecolor='none', zorder=5
    )
    ax.add_patch(pill)
    ax.text(x + 0.5, y + height - 0.24, f"STEP {step_num}", fontsize=7, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=6)
    
    # Title
    ax.text(x + 0.95, y + height - 0.24, title, fontsize=9.5, fontweight='bold', color='#0F172A', va='center', zorder=6)
    
    # Subtitle
    ax.text(x + 0.15, y + 0.35, subtitle, fontsize=8, color='#475569', zorder=6, linespacing=1.2)

def draw_diamond_decision(ax, cx, cy, size, text, color="#2563EB"):
    pts = [
        [cx, cy + size],
        [cx + size * 1.35, cy],
        [cx, cy - size],
        [cx - size * 1.35, cy]
    ]
    diamond = patches.Polygon(pts, facecolor='#FFFFFF', edgecolor=color, linewidth=2, zorder=5)
    ax.add_patch(diamond)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=8, fontweight='bold', color=color, zorder=6)

def draw_connector(ax, start, end, label=None, label_pos=None, color="#0F172A", style='solid'):
    ax.annotate(
        '', xy=end, xytext=start,
        arrowprops=dict(
            facecolor=color, edgecolor=color,
            arrowstyle='->,head_width=0.25,head_length=0.35',
            lw=1.6, linestyle=style
        ),
        zorder=7
    )
    if label and label_pos:
        ax.text(label_pos[0], label_pos[1], label, fontsize=8, fontweight='bold', color=color,
                bbox=dict(facecolor='white', edgecolor='#E2E8F0', boxstyle='round,pad=0.2', alpha=0.95), zorder=8)

# ── Title Banner ──
ax.text(9.0, 11.45, "SECURESIGN — END-TO-END SYSTEM WORKFLOW & ACTIVITY ARCHITECTURE", ha='center', va='center', fontsize=18, fontweight='bold', color='#0B132B')
ax.text(9.0, 11.05, "CCA India & IT Act 2000 Section 3A Compliant • Hardware-Level Digital Signature Lifecycle", ha='center', va='center', fontsize=11, fontstyle='italic', color='#64748B')

# ── Start Node ──
start_circle = patches.Circle((1.3, 9.4), radius=0.22, facecolor='#0F172A', edgecolor='#007AFF', linewidth=2, zorder=5)
ax.add_patch(start_circle)
ax.text(1.3, 9.0, "Start", ha='center', fontsize=8, fontweight='bold', color='#0F172A')

# ── Phase 1 Cards ──
draw_card(ax, 1.8, 8.8, 3.8, 1.1, "1", "Select PDF Document", "User picks document in Android app\nNative picker reads multi-page PDF", badge_color="#2563EB")
draw_connector(ax, (1.52, 9.4), (1.8, 9.4))

draw_card(ax, 1.8, 6.7, 3.8, 1.1, "2", "On-Device SHA-256 Hash", "Computes cryptographic 32-byte digest\nOriginal PDF remains secure on device", badge_color="#2563EB")
draw_connector(ax, (3.7, 8.8), (3.7, 7.8))

# ── Phase 2 Cards & Decision ──
draw_connector(ax, (5.6, 7.25), (6.8, 7.25))

draw_diamond_decision(ax, 7.6, 7.25, 0.45, "Token\nPlugged?", color="#7C3AED")

# Token No Branch
draw_card(ax, 6.8, 8.8, 4.4, 0.95, "X", "Alert: Plug Type-C Token", "Prompt user to connect USB DSC dongle\nHalts execution safely", badge_color="#EF4444", fill="#FEF2F2", edge="#EF4444")
draw_connector(ax, (7.6, 7.7), (7.6, 8.8), label="No", label_pos=(7.9, 8.2), color="#EF4444")

# Token Yes Branch
draw_card(ax, 9.0, 6.7, 2.3, 1.1, "3", "Enter PIN", "User inputs 8-digit PIN\nRAM zeroized immediately", badge_color="#7C3AED")
draw_connector(ax, (8.05, 7.25), (9.0, 7.25), label="Yes", label_pos=(8.5, 7.5), color="#059669")

# ── Phase 3 Cards & Decision ──
draw_connector(ax, (11.3, 7.25), (12.4, 7.25))

draw_diamond_decision(ax, 13.0, 7.25, 0.48, "PIN\nValid?", color="#D97706")

# PIN No Branch (Retry / Lock)
draw_card(ax, 12.2, 8.8, 4.6, 0.95, "!", "3 Failed PINs -> Token Lock", "Hardware locks at chip level (SW1=63)\nDefends against brute-force attacks", badge_color="#DC2626", fill="#FEF2F2", edge="#DC2626")
draw_connector(ax, (13.0, 7.73), (13.0, 8.8), label="No (>=3)", label_pos=(13.5, 8.2), color="#DC2626")

# Retry loop (<3)
ax.annotate(
    '', xy=(10.15, 7.8), xytext=(12.2, 9.27),
    arrowprops=dict(facecolor='#64748B', edgecolor='#64748B', arrowstyle='->', lw=1.3, linestyle='dashed'),
    zorder=7
)
ax.text(11.2, 8.7, "Retry (<3)", fontsize=7.5, color='#475569', fontweight='bold', bbox=dict(facecolor='white', edgecolor='none', pad=1))

# PIN Yes Branch: Step 4 On-Chip Signing
draw_card(ax, 14.2, 6.7, 2.7, 1.1, "4", "On-Chip RSA Signing", "FIPS 140-2 L3 Coprocessor signs hash\nPrivate Key NEVER leaves chip", badge_color="#D97706")
draw_connector(ax, (13.48, 7.25), (14.2, 7.25), label="Yes", label_pos=(13.8, 7.5), color="#059669")

# ── Transition from Phase 3 to Phase 4 (Flows Down) ──
draw_connector(ax, (15.55, 6.7), (15.55, 4.4))

# ── Phase 4 Cards (Bottom Row) ──
draw_card(ax, 13.6, 2.8, 3.2, 1.3, "5", "RFC 3161 TSA Timestamp", "Cloud backend requests trusted timestamp\nEmbeds legal proof of signing date/time", badge_color="#059669")

draw_card(ax, 9.6, 2.8, 3.6, 1.3, "6", "PAdES-LTV & Visible Seal", "pdf-lib preserves all original PDF pages\nStamps AP Govt CCA Class-3 visual seal", badge_color="#059669")
draw_connector(ax, (13.6, 3.45), (13.2, 3.45))

draw_card(ax, 5.6, 2.8, 3.6, 1.3, "7", "1-Tap Direct Download", "Downloads signed PDF to mobile device\nOpens instantly in Adobe Acrobat (Zero OTP)", badge_color="#059669")
draw_connector(ax, (9.6, 3.45), (9.2, 3.45))

draw_card(ax, 1.6, 2.8, 3.6, 1.3, "8", "Adobe Acrobat Validation", "Displays Green Ribbon: Signature VALID\n100% Legal Validity under IT Act Sec 3A", badge_color="#059669", fill="#F0FDF4", edge="#10B981")
draw_connector(ax, (5.6, 3.45), (5.2, 3.45))

# End Success Node
end_out = patches.Circle((1.0, 3.45), radius=0.28, facecolor='none', edgecolor='#059669', linewidth=2.5, zorder=5)
end_in = patches.Circle((1.0, 3.45), radius=0.18, facecolor='#059669', edgecolor='#059669', zorder=5)
ax.add_patch(end_out)
ax.add_patch(end_in)
draw_connector(ax, (1.6, 3.45), (1.3, 3.45))
ax.text(1.0, 2.85, "VERIFIED\nVALID", ha='center', fontsize=7.5, fontweight='bold', color='#059669')

# Bottom Summary Pill
leg = patches.FancyBboxPatch(
    (0.8, 0.4), 16.4, 0.6,
    boxstyle="round,pad=0.04,rounding_size=0.1",
    facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2, zorder=2
)
ax.add_patch(leg)
ax.text(9.0, 0.7, "GOVERNMENT OF ANDHRA PRADESH • RTIH • APIS • NIC INNOVATION CHALLENGE 2026 | SECURESIGN WORKFLOW SUITE", ha='center', va='center', fontsize=9, fontweight='bold', color='#1E293B')

plt.tight_layout()
out_png = 'uploads/SecureSign_Executive_Workflow_Diagram.png'
out_png_root = 'SecureSign_Executive_Workflow_Diagram.png'
plt.savefig(out_png, dpi=300, bbox_inches='tight')
plt.savefig(out_png_root, dpi=300, bbox_inches='tight')
plt.close()

print(f"Generated Executive PNG Diagram: {out_png}")

# ── 2. Create Word Document with Beautifully Formatted Visual Guide ──
doc = docx.Document()

for section in doc.sections:
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

# Title Header
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_p.add_run('SECURESIGN: EXECUTIVE WORKFLOW & ARCHITECTURE GUIDE\n')
title_run.bold = True
title_run.font.size = Pt(22)
title_run.font.color.rgb = RGBColor(11, 19, 43)

sub_run = title_p.add_run('Comprehensive Visual Process Flow, Security Guarantees & Evaluation Walkthrough\n')
sub_run.font.size = Pt(12)
sub_run.font.italic = True
sub_run.font.color.rgb = RGBColor(71, 85, 105)

meta_run = title_p.add_run('Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026\nLead Contact: pmahi7801@gmail.com | Live API: https://hackthonapp-production.up.railway.app\n')
meta_run.font.size = Pt(9.5)
meta_run.font.color.rgb = RGBColor(0, 122, 255)

doc.add_paragraph('─' * 75)

# Insert High-Resolution Graphic
p_img = doc.add_paragraph()
p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img.paragraph_format.space_before = Pt(6)
p_img.paragraph_format.space_after = Pt(10)
doc.add_picture(out_png, width=Inches(7.2))

# ── 4 Phases Executive Summary Table ──
p_t = doc.add_paragraph()
p_t.paragraph_format.space_before = Pt(10)
p_t.paragraph_format.space_after = Pt(6)
r_t = p_t.add_run('EXECUTIVE 4-PHASE PROCESS BREAKDOWN')
r_t.bold = True
r_t.font.size = Pt(13)
r_t.font.color.rgb = RGBColor(11, 19, 43)

phases_data = [
    ('Phase 1: Document Intake (Mobile Device)', '#2563EB', [
        ('Step 1: Pick PDF Document', 'User selects their multi-page PDF in the Android app. Native file picker loads document securely.'),
        ('Step 2: On-Device SHA-256 Hashing', 'Computes 32-byte mathematical SHA-256 digest on-device. The original document never leaves unencrypted (Zero Document Exposure).')
    ]),
    ('Phase 2: Hardware CCID Handshake (Type-C Token)', '#7C3AED', [
        ('Token Detection', 'Android USB Host API detects Smart Card CCID (USB Class 0x0B). If not connected, prompts user to plug in token.'),
        ('Step 3: Secure PIN Entry', 'User inputs 8-digit Token PIN. Formats ISO 7816-4 VERIFY APDU. RAM holding PIN is zeroized (0x00) immediately after execution (CCA Rule 2).')
    ]),
    ('Phase 3: On-Chip Signing (FIPS 140-2 Level 3)', '#D97706', [
        ('Step 4: On-Chip RSA-2048 Signing', 'Token coprocessor signs the SHA-256 digest on-chip. Private key NEVER leaves hardware crypto chip (CCA Rule 1).'),
        ('Brute-Force Protection', 'Token locks automatically after 3 consecutive wrong PIN attempts (SW1=0x63, CCA Rule 4).')
    ]),
    ('Phase 4: Cloud PAdES Assembly & Legal Delivery', '#059669', [
        ('Step 5: RFC 3161 TSA Timestamp', 'Cloud backend injects cryptographic timestamp token from a trusted Time Stamping Authority proving exact date/time (CCA Rule 3).'),
        ('Step 6: Visible Seal & PAdES Assembly', 'pdf-lib engine preserves 100% of original multi-page PDF pages and stamps the official AP Govt / CCA Class-3 seal on Page 2.'),
        ('Step 7 & 8: 1-Tap Download & Acrobat Verification', 'User taps Download ➔ Opens directly in Adobe Acrobat (Zero OTP). Displays Green Ribbon: "Signed and all signatures are valid".')
    ])
]

for phase_title, color_hex, steps in phases_data:
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Phase Header
    hdr = table.rows[0].cells
    hdr[0].width = Inches(2.2)
    hdr[1].width = Inches(4.8)
    hdr[0].text = phase_title
    hdr[1].text = 'Detailed Technical Action & Security Guarantee'
    
    for c in hdr:
        set_cell_background(c, color_hex.replace('#', ''))
        set_cell_margins(c, top=100, bottom=100, left=140, right=140)
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(255, 255, 255)
                
    for s_name, s_desc in steps:
        row = table.add_row().cells
        row[0].width = Inches(2.2)
        row[1].width = Inches(4.8)
        row[0].text = s_name
        row[1].text = s_desc
        
        set_cell_background(row[0], 'F8FAFC')
        set_cell_background(row[1], 'FFFFFF')
        set_cell_margins(row[0], top=80, bottom=80, left=120, right=120)
        set_cell_margins(row[1], top=80, bottom=80, left=120, right=120)
        
        for p in row[0].paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(15, 23, 42)
                
        for p in row[1].paragraphs:
            for r in p.runs:
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(51, 65, 85)
                
    doc.add_paragraph('') # spacing

# ── Summary & Evaluation Links ──
p_links = doc.add_paragraph()
p_links.add_run('Official Hackathon Submission References:\n').bold = True
p_links.add_run('• Production REST API: https://hackthonapp-production.up.railway.app\n')
p_links.add_run('• GitHub Source Code: https://github.com/mahankalikornepati2-netizen/hackthonapp\n')
p_links.add_run('• Compiled APK Build #4384cd86: https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c\n')
p_links.add_run('• Official Google Form: https://forms.gle/TJDYkF6feKFrywsd7\n')

out_docx = 'uploads/SecureSign_Executive_Workflow_Guide.docx'
out_docx_root = 'SecureSign_Executive_Workflow_Guide.docx'
doc.save(out_docx)
doc.save(out_docx_root)

print(f"Generated Executive Word Document: {out_docx}")
