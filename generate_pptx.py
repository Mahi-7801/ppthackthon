import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 widescreen format

    blank_layout = prs.slide_layouts[6] # blank layout

    # High-Contrast Agency-Grade Color Palette
    COLOR_BG = RGBColor(11, 15, 25)           # #0B0F19 Deep Obsidian
    COLOR_CARD = RGBColor(21, 29, 45)         # #151D2D Rich Dark Slate Card
    COLOR_CARD_ALT = RGBColor(26, 36, 56)     # #1A2438 Lighter Card
    COLOR_BORDER_EMERALD = RGBColor(16, 185, 129) # #10B981 Emerald
    COLOR_BORDER_CYAN = RGBColor(6, 182, 212)    # #06B6D4 Cyan
    COLOR_BORDER_RED = RGBColor(239, 68, 68)     # #EF4444 Red Accent
    COLOR_EMERALD = RGBColor(52, 211, 153)    # #34D399 Bright Emerald
    COLOR_CYAN = RGBColor(56, 189, 248)       # #38BDF8 Bright Sky Blue
    COLOR_GOLD = RGBColor(251, 191, 36)       # #FBBF24 Amber Gold
    COLOR_WHITE = RGBColor(255, 255, 255)     # #FFFFFF Pure White
    COLOR_TEXT_MUTED = RGBColor(203, 213, 225) # #CBD5E1 Bright Silver

    assets_dir = os.path.join(os.getcwd(), 'presentation_assets')

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

    def add_header(slide, tag_text, title_text, slide_num):
        set_slide_background(slide)
        
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = COLOR_BORDER_CYAN
        top_bar.line.fill.background()

        badge_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.4), Inches(0.35))
        badge_bg.fill.solid()
        badge_bg.fill.fore_color.rgb = RGBColor(16, 185, 129)
        badge_bg.line.fill.background()
        tf_badge = badge_bg.text_frame
        p_badge = tf_badge.paragraphs[0]
        p_badge.text = f"✦  {tag_text.upper()}"
        p_badge.font.size = Pt(11)
        p_badge.font.bold = True
        p_badge.font.color.rgb = RGBColor(0, 0, 0)
        p_badge.alignment = PP_ALIGN.CENTER

        num_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.2), Inches(0.35), Inches(1.3), Inches(0.35))
        num_bg.fill.solid()
        num_bg.fill.fore_color.rgb = COLOR_CARD
        num_bg.line.color.rgb = COLOR_BORDER_CYAN
        num_bg.line.width = Pt(1)
        tf_num = num_bg.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = f"{slide_num:02d} / 10"
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_CYAN
        p_num.alignment = PP_ALIGN.CENTER

        txBoxTitle = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tfTitle = txBoxTitle.text_frame
        pTitle = tfTitle.paragraphs[0]
        pTitle.text = title_text
        pTitle.font.size = Pt(26)
        pTitle.font.bold = True
        pTitle.font.color.rgb = COLOR_WHITE

        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(2.5), Inches(0.04))
        bar.fill.solid()
        bar.fill.fore_color.rgb = COLOR_EMERALD
        bar.line.fill.background()

    def add_card(slide, left, top, width, height, border_color=COLOR_BORDER_CYAN, accent_top=True):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        if accent_top:
            top_line = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
            top_line.fill.solid()
            top_line.fill.fore_color.rgb = border_color
            top_line.line.fill.background()
        return shape

    def add_image_card(slide, img_name, left, top, width, height, border_color=COLOR_BORDER_CYAN):
        img_path = os.path.join(assets_dir, img_name)
        if os.path.exists(img_path):
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
            card.fill.solid()
            card.fill.fore_color.rgb = COLOR_CARD
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)

            top_line = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
            top_line.fill.solid()
            top_line.fill.fore_color.rgb = border_color
            top_line.line.fill.background()

            # Set height proportionally to preserve aspect ratio without clipping
            pic = slide.shapes.add_picture(img_path, left + Inches(0.1), top + Inches(0.15), height=height - Inches(0.25))
            # Center picture inside container if narrower than card width
            if pic.width < (width - Inches(0.2)):
                pic.left = int(left + (width - pic.width) / 2)

    # ==========================================
    # SLIDE 1: HERO TITLE SLIDE (WITH LIVE SPLASH SCREEN)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    add_card(s1, Inches(0.8), Inches(1.0), Inches(7.5), Inches(5.8), COLOR_BORDER_EMERALD)

    t1 = s1.shapes.add_textbox(Inches(1.1), Inches(1.2), Inches(6.9), Inches(5.4))
    tf1 = t1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "✦ RTIH / APIS / NIC HACKATHON 2026"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    p2 = tf1.add_paragraph()
    p2.text = "Type-C DSC Mobile Signing Solution"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE

    p3 = tf1.add_paragraph()
    p3.text = "\nEnterprise-Grade Hardware Digital Signatures directly on Mobile & WebViews — eliminating desktop software dependencies."
    p3.font.size = Pt(15)
    p3.font.color.rgb = COLOR_TEXT_MUTED

    p4 = tf1.add_paragraph()
    p4.text = "\n✔ 100% CCA Guideline Compliant   ✔ Native Android & iOS CCID Stack"
    p4.font.size = Pt(12)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_EMERALD

    p_link = tf1.add_paragraph()
    p_link.text = "\n🚀 Live App Expo Build:\nhttps://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/a8104366-38b4-4f48-a4b1-8e4a2796ae66"
    p_link.font.size = Pt(11)
    p_link.font.bold = True
    p_link.font.color.rgb = COLOR_GOLD

    # Live Splash Screen Image
    add_image_card(s1, 'live_splash.jpeg', Inches(8.6), Inches(1.0), Inches(3.9), Inches(5.8), COLOR_BORDER_EMERALD)

    # ==========================================
    # SLIDE 2: THE PROBLEM
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement", "The Mobile Signing Bottleneck in e-Governance", 2)

    metric_card = add_card(s2, Inches(0.8), Inches(1.7), Inches(11.7), Inches(1.2), COLOR_BORDER_RED)
    tx_m = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.0))
    tf_m = tx_m.text_frame
    tf_m.word_wrap = True
    
    p = tf_m.paragraphs[0]
    p.text = "90%+ OF INDIAN DIGITAL SIGNATURES ARE TETHERED TO DESKTOP PCS"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_BORDER_RED
    
    p_sub = tf_m.add_paragraph()
    p_sub.text = "Class-3 DSC USB dongles require Windows drivers, breaking mobile-first governance for field officers & citizens."
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED

    c2 = add_card(s2, Inches(0.8), Inches(3.1), Inches(6.5), Inches(3.8), COLOR_BORDER_RED)
    tx2 = s2.shapes.add_textbox(Inches(1.0), Inches(3.3), Inches(6.1), Inches(3.4))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "🚨 Core Friction Points:"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    points2 = [
        ("Desktop Drivers Needed", "ePass2003, HYP2003, and Watchdata tokens lack mobile drivers."),
        ("OS Protocol Barrier", "Android Host API & iOS CryptoTokenKit are not built into web portals."),
        ("Broken Approvals", "District collectors & tender officers cannot approve documents on mobile tablets."),
        ("Cloud OTP Vulnerability", "Cloud signing compromises physical token key retention rules.")
    ]
    for title, desc in points2:
        p = tf2.add_paragraph()
        p.text = f"\n• {title}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    add_image_card(s2, 'problem_desktop_vs_mobile.png', Inches(7.6), Inches(3.1), Inches(4.9), Inches(3.8), COLOR_BORDER_RED)

    # ==========================================
    # SLIDE 3: SOLUTION OVERVIEW (WITH LIVE SIGNING CONFIRMATION SCREEN)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Solution Overview", "Direct Plug & Sign Mobile Hardware Integration", 3)

    # Live Signing Complete Screen
    add_image_card(s3, 'live_signature_complete.jpeg', Inches(0.8), Inches(1.7), Inches(3.8), Inches(5.2), COLOR_BORDER_EMERALD)

    sol_features = [
        ("🔌 Direct USB-C CCID Stack", "Native Kotlin USB Host driver + iOS CryptoTokenKit bridge communicates directly with smart card chips."),
        ("🌐 Hybrid WebView JS Bridge", "Injects window.DSCSigning into web portals so legacy e-Gov websites trigger USB signing in 5 lines of code."),
        ("🔒 PAdES & RFC 3161 Timestamping", "Assembles tamper-proof PAdES signatures with authoritative TSA timestamps and PostgreSQL audit tracking.")
    ]

    top_pos = 1.7
    for title, desc in sol_features:
        add_card(s3, Inches(4.9), Inches(top_pos), Inches(7.6), Inches(1.5), COLOR_BORDER_EMERALD)
        tx = s3.shapes.add_textbox(Inches(5.1), Inches(top_pos + 0.15), Inches(7.2), Inches(1.2))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        
        top_pos += 1.85

    # ==========================================
    # SLIDE 4: CCA COMPLIANCE MATRIX (WITH LIVE SETTINGS BADGE SCREEN)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Regulatory Blueprint", "100% CCA (Controller of Certifying Authorities) Compliance Matrix", 4)

    table_shape = s4.shapes.add_table(6, 4, Inches(0.8), Inches(1.7), Inches(8.0), Inches(5.2))
    table = table_shape.table
    
    headers = ["Rule #", "CCA Guideline Requirement", "Implementation in Solution", "Status"]
    col_widths = [Inches(1.0), Inches(2.6), Inches(3.1), Inches(1.3)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(16, 185, 129)
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = RGBColor(0, 0, 0)

    rows_data = [
        ("Rule 1", "Private key stays on token", "SHA-256 hash sent to token; signature computed inside chip via APDU", "VERIFIED"),
        ("Rule 2", "Secure PIN Handling", "PIN passed directly to smartcard memory; instant RAM zeroization", "VERIFIED"),
        ("Rule 3", "PAdES + RFC 3161", "Backend queries TSA & seals PDF with PAdES envelope", "VERIFIED"),
        ("Rule 4", "Enforce Lockout Policy", "Honors token retry limits; hard lockout after 3 incorrect attempts", "VERIFIED"),
        ("Rule 5", "Full Audit Trail", "Immutable PostgreSQL session audit logging with serial & IP tracking", "VERIFIED")
    ]

    for row_idx, row_content in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(row_content):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            bg = COLOR_CARD if row_idx % 2 == 1 else COLOR_CARD_ALT
            cell.fill.fore_color.rgb = bg
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                if col_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_GOLD
                elif col_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_EMERALD
                else:
                    p.font.color.rgb = COLOR_WHITE

    # Live Settings & CCA Compliance Image
    add_image_card(s4, 'live_settings_cca.jpeg', Inches(9.1), Inches(1.7), Inches(3.4), Inches(5.2), COLOR_BORDER_EMERALD)

    # ==========================================
    # SLIDE 5: SYSTEM ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Architecture & Tech Stack", "Dual-Layer Mobile & Cloud Architecture", 5)

    # 4 Stacked Architecture Layer Cards on Left
    arch_layers = [
        ("📱 Layer 1: Mobile UI & WebView Bridge", "React Native, Expo, JS Bridge, PIN Modal", COLOR_BORDER_CYAN),
        ("🔌 Layer 2: Native Smartcard Transport", "Kotlin USB Host API, CcidTransport, iOS CryptoTokenKit", COLOR_BORDER_EMERALD),
        ("🔒 Layer 3: Hardware Token Chip", "Type-C CCID Dongle, APDU RSA Hashing, 3-Attempt Lockout", COLOR_GOLD),
        ("☁️ Layer 4: Cloud Backend Services", "Express SHA-256 Hasher, RFC 3161 TSA, PostgreSQL Audit Log", COLOR_BORDER_CYAN)
    ]

    top_pos_arch = 1.7
    for title, desc, border_col in arch_layers:
        add_card(s5, Inches(0.8), Inches(top_pos_arch), Inches(5.6), Inches(1.15), border_col)
        tx = s5.shapes.add_textbox(Inches(1.0), Inches(top_pos_arch + 0.1), Inches(5.2), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = border_col

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        
        top_pos_arch += 1.35

    img5_path = os.path.join(assets_dir, 'system_architecture_diagram.png')
    add_image_card(s5, 'system_architecture_diagram.png', Inches(6.7), Inches(1.7), Inches(5.8), Inches(5.2), COLOR_BORDER_CYAN)

    # ==========================================
    # SLIDE 6: LIVE MOBILE APP USER FLOW (WITH LIVE PIN ENTRY SCREEN)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Mobile App User Flow", "5-Screen Live Mobile Signing Experience Flow", 6)

    # Live Access Document / PIN Screen
    add_image_card(s6, 'live_pin_entry.jpeg', Inches(0.8), Inches(1.7), Inches(3.6), Inches(5.2), COLOR_BORDER_EMERALD)

    c6 = add_card(s6, Inches(4.7), Inches(1.7), Inches(7.8), Inches(5.2), COLOR_BORDER_EMERALD)
    tx6 = s6.shapes.add_textbox(Inches(4.9), Inches(1.9), Inches(7.4), Inches(4.8))
    tf6 = tx6.text_frame
    tf6.word_wrap = True
    
    p = tf6.paragraphs[0]
    p.text = "📲 Live App Execution Flow (Screen Navigation):"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    screen_steps = [
        ("1. HomeScreen", "🔌 Token Auto-Detection: Detects plugged Type-C USB DSC dongle via native CCID transport driver."),
        ("2. PINEntryScreen", "🔐 Secure PIN Input: Passes PIN directly to hardware token memory with instant RAM zeroization."),
        ("3. DocumentSelect", "📄 Hash Generation: Selects target PDF document & computes SHA-256 digest locally."),
        ("4. SignConfirmation", "✍️ Hardware Sign & Audit: Token signs hash via RSA APDU; TSA attaches timestamp & logs to PostgreSQL.")
    ]
    for scr_name, desc in screen_steps:
        p = tf6.add_paragraph()
        p.text = f"\n• {scr_name} — "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 7: SECURITY & DEFENSE
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Security Engine", "Defense-in-Depth Hardware & Data Protection", 7)

    # ==========================================
    # SLIDE 7: SECURITY ENGINE
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Security Engine", "Defense-in-Depth Hardware & Data Protection", 7)

    c7_a = add_card(s7, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), COLOR_BORDER_CYAN)
    tx7_a = s7.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.2), Inches(4.8))
    tf7_a = tx7_a.text_frame
    tf7_a.word_wrap = True
    tf7_a.paragraphs[0].text = "🔒 Hardware Security Engine"
    tf7_a.paragraphs[0].font.size = Pt(18)
    tf7_a.paragraphs[0].font.bold = True
    tf7_a.paragraphs[0].font.color.rgb = COLOR_CYAN
    
    pts7_a = [
        ("On-Chip Key Isolation", "Private RSA 2048 / ECC keys are non-exportable hardware assets inside silicon."),
        ("RAM Zeroization", "Sensitive PIN byte arrays purged immediately after APDU transmission."),
        ("3-Attempt Lockout", "App respects physical token policy; hard lockout after 3 incorrect attempts.")
    ]
    for title, desc in pts7_a:
        p = tf7_a.add_paragraph()
        p.text = f"\n• {title}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    c7_b = add_card(s7, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.2), COLOR_BORDER_EMERALD)
    tx7_b = s7.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.2), Inches(4.8))
    tf7_b = tx7_b.text_frame
    tf7_b.word_wrap = True
    tf7_b.paragraphs[0].text = "🛡️ Cryptographic Sealing"
    tf7_b.paragraphs[0].font.size = Pt(18)
    tf7_b.paragraphs[0].font.bold = True
    tf7_b.paragraphs[0].font.color.rgb = COLOR_EMERALD
    
    pts7_b = [
        ("SHA-256 Hashing Standard", "Standardized collision-resistant document hashing algorithm."),
        ("RFC 3161 TSA Timestamp", "Cryptographically verifiable proof from CCA-approved Timestamp Authority."),
        ("PostgreSQL Audit RLS", "User-isolated session audit database policies with serial & IP tracking.")
    ]
    for title, desc in pts7_b:
        p = tf7_b.add_paragraph()
        p.text = f"\n• {title}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 8: WEBVIEW BRIDGE & AUTH (WITH LIVE LOGIN SCREEN)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Developer Integration", "Hybrid Mobile WebView & Auth Stack", 8)

    # Live Login Screen
    add_image_card(s8, 'live_login.jpeg', Inches(0.8), Inches(1.7), Inches(3.6), Inches(5.2), COLOR_BORDER_CYAN)

    c8_b = add_card(s8, Inches(4.7), Inches(1.7), Inches(7.8), Inches(5.2), COLOR_BORDER_CYAN)
    tx8_b = s8.shapes.add_textbox(Inches(4.9), Inches(1.9), Inches(7.4), Inches(4.8))
    tf8_b = tx8_b.text_frame
    tf8_b.word_wrap = True
    tf8_b.paragraphs[0].text = "🌐 Hybrid Mobile WebView JavaScript Bridge:"
    tf8_b.paragraphs[0].font.size = Pt(18)
    tf8_b.paragraphs[0].font.bold = True
    tf8_b.paragraphs[0].font.color.rgb = COLOR_CYAN
    
    pts8_b = [
        ("Zero Portal Changes", "Legacy government portals invoke window.DSCSigning.signDocument()."),
        ("Seamless Native Handshake", "WebView intercepts command & triggers native Type-C USB CCID module."),
        ("Drop-in Mobile SDK", "Exposed via React Native Bridge DSCSigningModule.kt & DSCSigningModule.swift."),
        ("Built-in User Auth", "Secure Supabase / InsForge JWT authentication for multi-tenant users.")
    ]
    for title, desc in pts8_b:
        p = tf8_b.add_paragraph()
        p.text = f"\n• {title}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 9: SYSTEM SEQUENCE DIAGRAM
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Sequence Diagram & Flow", "Step-by-Step Hardware Handshake & Download Gate", 9)

    c9_left = add_card(s9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), COLOR_BORDER_CYAN)
    tx9_l = s9.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.2), Inches(4.8))
    tf9_l = tx9_l.text_frame
    tf9_l.word_wrap = True
    tf9_l.paragraphs[0].text = "🔄 App Sequence Steps (1 - 4)"
    tf9_l.paragraphs[0].font.size = Pt(18)
    tf9_l.paragraphs[0].font.bold = True
    tf9_l.paragraphs[0].font.color.rgb = COLOR_CYAN

    seq_left = [
        ("1. User -> LoginScreen", "Sign In & Navigate to Home Screen."),
        ("2. User -> HomeScreen", "Connect Class-3 Type-C USB Dongle Token."),
        ("3. HomeScreen -> PINEntry", "Tap 'Proceed to PIN Entry' & input token PIN."),
        ("4. PIN -> DocumentSelect", "PIN verified on token -> Generate pre-signature SHA-256 digest.")
    ]
    for title, desc in seq_left:
        p = tf9_l.add_paragraph()
        p.text = f"\n• {title}: "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    c9_right = add_card(s9, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.2), COLOR_BORDER_EMERALD)
    tx9_r = s9.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.2), Inches(4.8))
    tf9_r = tx9_r.text_frame
    tf9_r.word_wrap = True
    tf9_r.paragraphs[0].text = "🔒 App Sequence Steps (5 - 7)"
    tf9_r.paragraphs[0].font.size = Pt(18)
    tf9_r.paragraphs[0].font.bold = True
    tf9_r.paragraphs[0].font.color.rgb = COLOR_EMERALD

    seq_right = [
        ("5. User -> SignConfirmation", "Tap 'Sign Document' -> Generate SHA256WithRSA hardware signature hex."),
        ("6. Sign -> Backend & DB", "Persist signed PDF, session & immutable audit log; session auto-invalidated."),
        ("7. SecureDoc -> PIN Gate", "🔒 Re-prompt PIN to authenticate hardware token -> 🔓 Unlock & download signed PDF.")
    ]
    for title, desc in seq_right:
        p = tf9_r.add_paragraph()
        p.text = f"\n• {title}: "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 10: CONCLUSION
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Future Vision & Conclusion", "Empowering Mobile-First Digital Trust", 10)

    # 3-Phase Roadmap Box Left
    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), COLOR_BORDER_CYAN)
    tx10_a = s10.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.2), Inches(4.8))
    tf10_a = tx10_a.text_frame
    tf10_a.word_wrap = True
    tf10_a.paragraphs[0].text = "🌟 3-Phase Product Roadmap"
    tf10_a.paragraphs[0].font.size = Pt(18)
    tf10_a.paragraphs[0].font.bold = True
    tf10_a.paragraphs[0].font.color.rgb = COLOR_CYAN
    
    pts10_a = [
        ("Phase 1 (Completed)", "USB-C CCID Native Stack + React Native App + PAdES + Audit Ledger."),
        ("Phase 2 (Q4 2026)", "Contactless NFC Smart Cards & Bluetooth Low Energy (BLE) Wireless Dongles."),
        ("Phase 3 (Q1 2027)", "National Digital India & NIC Portal Plugin SDK Distribution.")
    ]
    for title, desc in pts10_a:
        p = tf10_a.add_paragraph()
        p.text = f"\n• {title}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED

    # Executive Summary Card Right
    c10_b = add_card(s10, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.2), COLOR_BORDER_EMERALD)
    tx10_b = s10.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.2), Inches(4.8))
    tf10_b = tx10_b.text_frame
    tf10_b.word_wrap = True
    
    p = tf10_b.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    
    p2 = tf10_b.add_paragraph()
    p2.text = "Type-C DSC Mobile Signing Solution"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE

    p_sub = tf10_b.add_paragraph()
    p_sub.text = "Empowering India's Mobile-First Infrastructure with Hardware-Grade Trust."
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED

    p_link10 = tf10_b.add_paragraph()
    p_link10.text = "\n🚀 Live Mobile App Expo Build:\nhttps://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/a8104366-38b4-4f48-a4b1-8e4a2796ae66"
    p_link10.font.size = Pt(11)
    p_link10.font.bold = True
    p_link10.font.color.rgb = COLOR_GOLD

    p3 = tf10_b.add_paragraph()
    p3.text = "\n✦ Ready for Judges' Q&A"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_EMERALD

    paths = [
        os.path.join(os.getcwd(), 'DSC_Mobile_Signing_Master_Deck.pptx'),
        os.path.join(os.getcwd(), 'DSC_Mobile_Signing_UserFlow_Deck.pptx')
    ]
    for out_path in paths:
        try:
            prs.save(out_path)
            print(f"SUCCESS: Saved live screenshots presentation deck at {out_path}")
        except Exception as e:
            print(f"Warning could not save to {out_path}: {e}")

if __name__ == '__main__':
    create_presentation()
