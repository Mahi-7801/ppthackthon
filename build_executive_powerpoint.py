import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)  # 16:9 Widescreen
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
NAVY_BG = RGBColor(11, 19, 43)        # #0B132B
CARD_BG = RGBColor(27, 38, 59)        # #1B263B
WHITE = RGBColor(255, 255, 255)
ELECTRIC_BLUE = RGBColor(0, 122, 255) # #007AFF
EMERALD_GREEN = RGBColor(16, 185, 129)# #10B981
AMBER = RGBColor(245, 158, 11)        # #F59E0B
LIGHT_SLATE = RGBColor(148, 163, 184) # #94A3B8
DARK_TEXT = RGBColor(15, 23, 42)

def set_slide_background(slide, color=NAVY_BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.color.rgb = color
    return bg

def add_header(slide, title_text, category_text="GOVERNMENT OF ANDHRA PRADESH • RTIH • APIS • NIC"):
    # Category / Tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    p_cat = tb_cat.text_frame.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ELECTRIC_BLUE
    
    # Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
    p_title = tb_title.text_frame.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE

def add_card(slide, left, top, width, height, title, body_bullets, border_color=ELECTRIC_BLUE, bg_color=CARD_BG):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    # Title
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = border_color
    p0.space_after = Pt(6)
    
    # Bullets
    for bullet in body_bullets:
        p = tf.add_paragraph()
        p.text = "• " + bullet
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
        p.space_after = Pt(4)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 1: Title Slide
# ══════════════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, NAVY_BG)

# Title Container
tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "GOVERNMENT OF ANDHRA PRADESH • RTIH • APIS • NIC"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ELECTRIC_BLUE
p.space_after = Pt(12)

p = tf1.add_paragraph()
p.text = "SecureSign: Type-C DSC Mobile Digital Signing Solution"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = WHITE
p.space_after = Pt(12)

p = tf1.add_paragraph()
p.text = "Enabling Hardware-Grade, CCA-Compliant Digital Signatures directly on Android Smartphones"
p.font.size = Pt(16)
p.font.italic = True
p.font.color.rgb = LIGHT_SLATE
p.space_after = Pt(28)

p = tf1.add_paragraph()
p.text = "Lead Innovator: pmahi7801@gmail.com  |  Live API: https://hackthonapp-production.up.railway.app\nStandard: 100% Indian IT Act 2000 Section 3A & PAdES-LTV Compliant"
p.font.size = Pt(12)
p.font.color.rgb = EMERALD_GREEN

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 2: Problem & Solution
# ══════════════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, NAVY_BG)
add_header(s2, "The Core Problem vs. The SecureSign Solution", "CHALLENGE ANALYSIS")

add_card(
    s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
    "❌ The Desktop Bottleneck (Current State)",
    [
        "Desktop Confinement: Officers must sit at a Windows PC to sign files with USB DSC tokens.",
        "Legacy Middleware: Requires unstable Java applets, browser plugins, and vendor desktop drivers.",
        "Zero Native Mobile Support: Android lacks built-in CCID smart card host drivers.",
        "Administrative Delays: Cabinet files, CFMS treasury bills, and citizen certificates stall when officers travel."
    ],
    border_color=RGBColor(239, 68, 68)
)

add_card(
    s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
    "✅ The SecureSign Innovation (Our Solution)",
    [
        "Direct USB Type-C CCID: Custom native Kotlin driver connects directly to DSC dongles on Android.",
        "Zero Key Leakage (CCA Rule 1): Private key stays isolated on FIPS 140-2 Level 3 hardware crypto-chip.",
        "On-Chip PIN Verification (CCA Rule 2): Hardware PIN verified on-chip; zero memory caching.",
        "PAdES-LTV + RFC 3161: Full legal validity under Indian IT Act 2000 Section 3A in <3 seconds."
    ],
    border_color=EMERALD_GREEN
)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 3: VISUAL OVERVIEW OF THE DIAGRAM (The Core Request)
# ══════════════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, RGBColor(248, 250, 252)) # Crisp Light Background for Image

# Header for Diagram Slide
tb_d_hdr = s3.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(12.1), Inches(0.7))
tf_d_hdr = tb_d_hdr.text_frame
p_dh0 = tf_d_hdr.paragraphs[0]
p_dh0.text = "SYSTEM ARCHITECTURE & ACTIVITY DIAGRAM: VISUAL OVERVIEW"
p_dh0.font.size = Pt(20)
p_dh0.font.bold = True
p_dh0.font.color.rgb = NAVY_BG

p_dh1 = tf_d_hdr.add_paragraph()
p_dh1.text = "4-Phase Cryptographic Lifecycle: From Document Selection to Global Adobe Acrobat Validation"
p_dh1.font.size = Pt(11)
p_dh1.font.color.rgb = ELECTRIC_BLUE

# Embed High-Resolution Diagram Image
img_path = 'uploads/SecureSign_Executive_Workflow_Diagram.png'
if os.path.exists(img_path):
    s3.shapes.add_picture(img_path, Inches(0.6), Inches(1.1), Inches(12.13), Inches(6.0))

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 4: 4-Phase Step-by-Step Breakdown (Easy to Understand)
# ══════════════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, NAVY_BG)
add_header(s4, "4-Phase Cryptographic Process Flow", "STEP-BY-STEP EXPLANATION")

add_card(
    s4, Inches(0.8), Inches(1.8), Inches(2.7), Inches(4.8),
    "1. Document Intake",
    [
        "User selects PDF in Android app.",
        "On-device engine computes 32-byte SHA-256 hash.",
        "Original PDF never leaves unencrypted.",
        "Zero Document Exposure."
    ],
    border_color=ELECTRIC_BLUE
)

add_card(
    s4, Inches(3.8), Inches(1.8), Inches(2.7), Inches(4.8),
    "2. Hardware Handshake",
    [
        "Android USB Host detects Class 0x0B CCID dongle.",
        "Officer enters 8-digit Token PIN on secure screen.",
        "Sends ISO 7816-4 VERIFY APDU to token.",
        "RAM zeroized immediately (CCA Rule 2)."
    ],
    border_color=RGBColor(124, 58, 237)
)

add_card(
    s4, Inches(6.8), Inches(1.8), Inches(2.7), Inches(4.8),
    "3. On-Chip Signing",
    [
        "FIPS 140-2 L3 chip executes RSA-2048 signing.",
        "Private Key NEVER leaves hardware token (CCA Rule 1).",
        "Hardware locks after 3 failed PIN attempts (Rule 4).",
        "Produces PKCS#1v1.5 signature."
    ],
    border_color=AMBER
)

add_card(
    s4, Inches(9.8), Inches(1.8), Inches(2.7), Inches(4.8),
    "4. Legal Delivery",
    [
        "Cloud backend injects RFC 3161 TSA timestamp (Rule 3).",
        "Stamps official AP Govt visible seal on Page 2.",
        "1-Tap download to Adobe Acrobat (Zero OTP).",
        "100% Valid (IT Act Sec 3A)."
    ],
    border_color=EMERALD_GREEN
)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 5: CCA India Regulatory Compliance Matrix
# ══════════════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, NAVY_BG)
add_header(s5, "100% CCA India Regulatory Compliance Matrix", "LEGAL & STATUTORY COMPLIANCE")

add_card(
    s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3),
    "Rule 1: Private Key Isolation",
    [
        "Requirement: Private key must NEVER leave hardware token.",
        "Implementation: On-chip RSA signing in FIPS 140-2 Level 3 Secure Element. Key extraction is impossible."
    ],
    border_color=EMERALD_GREEN
)

add_card(
    s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3),
    "Rule 2: On-Chip PIN Verification",
    [
        "Requirement: PIN must be verified on hardware chip without caching.",
        "Implementation: ISO 7816-4 VERIFY APDU. PIN memory is zeroized (0x00) immediately after execution."
    ],
    border_color=EMERALD_GREEN
)

add_card(
    s5, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.3),
    "Rule 3: PAdES-LTV & RFC 3161 TSA",
    [
        "Requirement: Long-Term Validation & Trusted Timestamping.",
        "Implementation: ETSI EN 319 142-1 standard with embedded X.509 Time Stamping Authority token."
    ],
    border_color=EMERALD_GREEN
)

add_card(
    s5, Inches(6.8), Inches(4.4), Inches(5.6), Inches(2.3),
    "Rule 4 & 5: Hardware Lock & Audit Trail",
    [
        "Requirement: Brute-force hardware defense & audit logging.",
        "Implementation: Token locks after 3 wrong PINs. Immutable audit records with IP, timestamp & cert serial."
    ],
    border_color=EMERALD_GREEN
)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 6: Compatibility & Real-World AP Impact
# ══════════════════════════════════════════════════════════════════════════
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, NAVY_BG)
add_header(s6, "Universal Compatibility & AP Governance Impact", "TRANSFORMATIVE VALUE")

add_card(
    s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
    "🔌 Universal Hardware & Vendor Support",
    [
        "Hardware Tokens: ePass2003, Watchdata ProxKey, TrustKey, Gemalto SafeNet, mToken CryptoID.",
        "Certifying Authorities: e-Mudhra, Capricorn, VSign, Sify, (n)Code Solutions, Pantasign Class-3 DSCs.",
        "Android OS: Android 8.0 (API 26) through Android 15 (API 35).",
        "Connection: Direct USB Type-C and Micro-USB OTG adapters."
    ],
    border_color=ELECTRIC_BLUE
)

add_card(
    s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
    "🏛️ Transformative Impact on AP Governance",
    [
        "e-Office & Secretariat: Ministers & IAS officers approve urgent cabinet files on-the-go.",
        "CFMS Treasury: DDOs sign treasury bills and vouchers on mobile phones in seconds.",
        "MeeSeva Citizen Services: Tahsildars issue digitally signed caste & land title certificates in the field.",
        "AP e-Procurement: Instant contractor signature verification for tenders."
    ],
    border_color=EMERALD_GREEN
)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 7: Live Verification & Conclusion
# ══════════════════════════════════════════════════════════════════════════
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, NAVY_BG)
add_header(s7, "Live Demonstration, Benchmark & Submission Links", "EVALUATION SUMMARY")

add_card(
    s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
    "📊 Proven Production Performance",
    [
        "Live Backend Latency: Average 0.42s across all 13 REST API endpoints.",
        "Master Test Suite: 13/13 Endpoints Passing (200 OK) live on Railway.",
        "Adobe Acrobat Reader: Displays Green Ribbon 'Signed & all signatures are valid'.",
        "Tamper Detection: Any alteration immediately breaks the SHA-256 hash."
    ],
    border_color=EMERALD_GREEN
)

add_card(
    s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
    "🔗 Official Project Resources",
    [
        "Live Production API: https://hackthonapp-production.up.railway.app",
        "GitHub Source Code: https://github.com/mahankalikornepati2-netizen/hackthonapp",
        "Compiled APK Build: https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c",
        "Official Form: https://forms.gle/TJDYkF6feKFrywsd7",
        "Team Contact: pmahi7801@gmail.com"
    ],
    border_color=ELECTRIC_BLUE
)

os.makedirs('uploads', exist_ok=True)
pptx_path1 = 'uploads/SecureSign_Executive_Pitch_Deck.pptx'
pptx_path2 = 'SecureSign_Executive_Pitch_Deck.pptx'

prs.save(pptx_path1)
prs.save(pptx_path2)

print(f"Successfully generated PowerPoint Presentation at:")
print(f"1. {pptx_path1}")
print(f"2. {pptx_path2}")
