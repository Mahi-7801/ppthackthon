import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

os.makedirs('uploads', exist_ok=True)

# ── 1. Generate High-Resolution Tools & Component Flowchart Graphic ──
fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Background
ax.add_patch(patches.Rectangle((0, 0), 16, 10, facecolor='#F8FAFC', zorder=0))

# Title Header
ax.text(8.0, 9.4, "SECURESIGN — TOOLS, FRAMEWORKS & PROTOCOL ARCHITECTURE", ha='center', va='center', fontsize=16, fontweight='bold', color='#0B132B')
ax.text(8.0, 9.0, "Complete Component Inventory & Data Exchange Stack across all 5 System Layers", ha='center', va='center', fontsize=10, fontstyle='italic', color='#64748B')

def draw_tool_box(ax, x, y, width, height, layer_title, tech_list, color_hex, tag_text):
    # Card Shadow
    shadow = patches.FancyBboxPatch(
        (x + 0.04, y - 0.04), width, height,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        facecolor='#CBD5E1', edgecolor='none', alpha=0.5, zorder=1
    )
    ax.add_patch(shadow)
    
    # Main Card
    card = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        facecolor='#FFFFFF', edgecolor=color_hex, linewidth=1.8, zorder=2
    )
    ax.add_patch(card)
    
    # Header Ribbon
    hdr = patches.FancyBboxPatch(
        (x, y + height - 0.6), width, 0.6,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor=color_hex, edgecolor='none', zorder=3
    )
    ax.add_patch(hdr)
    ax.text(x + 0.25, y + height - 0.3, layer_title, fontsize=10.5, fontweight='bold', color='#FFFFFF', va='center', zorder=4)
    ax.text(x + width - 0.25, y + height - 0.3, tag_text, fontsize=8, fontweight='bold', color='#FFFFFF', va='center', ha='right', zorder=4)
    
    # Bullet text
    for idx, t in enumerate(tech_list):
        ax.text(x + 0.25, y + height - 0.95 - idx * 0.45, f"• {t}", fontsize=8.5, color='#334155', zorder=4)

# 5 Layer Cards
draw_tool_box(
    ax, 0.8, 1.2, 2.7, 7.2,
    "1. MOBILE CLIENT",
    [
        "React Native 0.74+",
        "TypeScript 5.x",
        "Expo SDK 51",
        "EAS Cloud Build",
        "expo-document-picker",
        "expo-crypto (SHA-256)",
        "React Navigation v6",
        "React Native Paper",
        "Lucide Modern Icons",
        "Hermes JS Engine",
        "Session Watchdog"
    ],
    "#2563EB", "UI / UX"
)

draw_tool_box(
    ax, 3.8, 1.2, 2.7, 7.2,
    "2. NATIVE DRIVER",
    [
        "Kotlin 1.9+",
        "Android USB Host API",
        "android.hardware.usb",
        "UsbManager Subsystem",
        "CcidTransport.kt",
        "P11Wrapper.kt",
        "DSCSigningModule.kt",
        "JNI Bridge Layer",
        "Bulk IN (0x82)",
        "Bulk OUT (0x02)",
        "5000ms Watchdog"
    ],
    "#7C3AED", "USB CCID"
)

draw_tool_box(
    ax, 6.8, 1.2, 2.7, 7.2,
    "3. HARDWARE TOKEN",
    [
        "ISO/IEC 7816-4 APDU",
        "PKCS#11 v2.40 API",
        "PKCS#15 Token Format",
        "FIPS 140-2 Level 3",
        "CC EAL 5+ Secure Elem",
        "RSA-2048 / 4096-bit",
        "ECDSA NIST P-256",
        "On-Chip Private Key",
        "On-Chip PIN Verify",
        "Hardware Lock (SW=63)",
        "Zero Key Leakage"
    ],
    "#D97706", "CRYPTO CHIP"
)

draw_tool_box(
    ax, 9.8, 1.2, 2.7, 7.2,
    "4. CLOUD PAdES",
    [
        "Node.js v20 LTS",
        "Express.js REST API",
        "pdf-lib PDF Engine",
        "Native Node Crypto",
        "RFC 3161 TSA Client",
        "X.509 Timestamp Token",
        "PAdES-LTV Container",
        "ByteRange Hash Lock",
        "AP Govt Visible Seal",
        "HTTPS TLS 1.3",
        "Sub-second Latency"
    ],
    "#059669", "ASSEMBLY"
)

draw_tool_box(
    ax, 12.8, 1.2, 2.7, 7.2,
    "5. COMPLIANCE",
    [
        "Adobe Acrobat Reader",
        "CCA Trust Store",
        "IT Act 2000 Sec 3A",
        "ETSI EN 319 142-1",
        "Supabase Postgres 15",
        "Row-Level Security",
        "JWT Bearer Auth",
        "Cryptographic Audit",
        "Railway Cloud Host",
        "e-Office / CFMS API",
        "100% Legally Valid"
    ],
    "#0284C7", "VERIFICATION"
)

# Connecting Arrows
for i in range(4):
    ax.annotate(
        '', xy=(3.8 + i * 3.0, 4.8), xytext=(3.5 + i * 3.0, 4.8),
        arrowprops=dict(facecolor='#0F172A', edgecolor='#0F172A', arrowstyle='->,head_width=0.2,head_length=0.3', lw=1.5),
        zorder=5
    )

plt.tight_layout()
tools_png = 'uploads/SecureSign_Tools_Architecture_Diagram.png'
plt.savefig(tools_png, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated Tools Graphic: {tools_png}")

# ── 2. Create Master PDF using ReportLab ──
pdf_path = 'uploads/SecureSign_Tools_and_Components_Workflow_Specification.pdf'
pdf_doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#0B132B'),
    alignment=1, # Center
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#2563EB'),
    alignment=1,
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=16,
    textColor=colors.HexColor('#0B132B'),
    spaceBefore=10,
    spaceAfter=6
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#334155'),
    spaceAfter=6
)

story = []

# Title & Meta
story.append(Paragraph("SECURESIGN: TOOLS, FRAMEWORKS & PROTOCOL SPECIFICATION", title_style))
story.append(Paragraph("Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026<br/>Lead Contact: pmahi7801@gmail.com | Production API: https://hackthonapp-production.up.railway.app", subtitle_style))
story.append(Spacer(1, 6))

# Embedded Visual Architecture Diagram
story.append(Paragraph("1. Tools, Frameworks & Component Architecture Diagram", h1_style))
story.append(RLImage(tools_png, width=7.2*inch, height=4.5*inch))
story.append(Spacer(1, 10))

# Component Breakdown Table
story.append(Paragraph("2. Detailed Component & Protocol Inventory", h1_style))

table_data = [
    [Paragraph("<b>Layer / Tier</b>", body_style), Paragraph("<b>Frameworks, SDKs & Libraries</b>", body_style), Paragraph("<b>Implementation Role & Guarantees</b>", body_style)],
    [Paragraph("<b>1. Mobile Client</b>", body_style), Paragraph("React Native 0.74+, TypeScript, Expo SDK 51, React Navigation, expo-document-picker, expo-crypto", body_style), Paragraph("Cross-platform mobile UI/UX, native file picking, on-device SHA-256 hashing, 1-tap PDF download (Zero OTP).", body_style)],
    [Paragraph("<b>2. Native Driver</b>", body_style), Paragraph("Kotlin 1.9+, android.hardware.usb, UsbManager, CcidTransport.kt, P11Wrapper.kt", body_style), Paragraph("Direct USB Type-C CCID host driver claiming Class 0x0B endpoints (0x82/0x02), managing APDUs without desktop drivers.", body_style)],
    [Paragraph("<b>3. Hardware Chip</b>", body_style), Paragraph("ISO 7816-4 APDU, PKCS#11 v2.40, FIPS 140-2 Level 3, CC EAL 5+ Secure Element", body_style), Paragraph("On-chip RSA-2048 private key signing, on-chip PIN verification, hardware brute-force defense. Zero key leakage.", body_style)],
    [Paragraph("<b>4. Cloud Backend</b>", body_style), Paragraph("Node.js v20 LTS, Express.js REST API, pdf-lib, RFC 3161 TSA Client, HTTPS TLS 1.3", body_style), Paragraph("Constructs PAdES-LTV containers, injects trusted X.509 timestamp token, stamps official AP Govt visible seal.", body_style)],
    [Paragraph("<b>5. Compliance</b>", body_style), Paragraph("Adobe Acrobat Reader, IT Act 2000 Section 3A, ETSI EN 319 142-1, Railway Cloud Host", body_style), Paragraph("100% legal admissibility in Indian courts, displays Green Checkmark ribbon worldwide.", body_style)]
]

t = Table(table_data, colWidths=[1.3*inch, 2.5*inch, 3.4*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B132B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 10))

# Links
story.append(Paragraph("<b>Official Verification & Repository References:</b><br/>"
                       "• Production API: https://hackthonapp-production.up.railway.app<br/>"
                       "• GitHub Repository: https://github.com/mahankalikornepati2-netizen/hackthonapp<br/>"
                       "• Standalone APK (Build #4384cd86): https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c", body_style))

pdf_doc.build(story)
print(f"Generated Lightweight High-Design PDF at: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
