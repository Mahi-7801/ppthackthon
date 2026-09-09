# 🏛️ SecureSign: Architecture & Workflow Diagrams

**Government of Andhra Pradesh • RTIH • APIS • NIC Innovation Challenge 2026**  
**Lead Contact**: `pmahi7801@gmail.com`  
**Live API**: `https://hackthonapp-production.up.railway.app`  
**GitHub**: `https://github.com/mahankalikornepati2-netizen/hackthonapp`

---

## 1. High-Level Multi-Tier System Architecture

```
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
```

---

## 2. End-to-End Cryptographic Sequence Flow

```
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
```

---

## 3. ISO 7816-4 Smart Card APDU Protocol Stack

| APDU Command | Hex Header (CLA INS P1 P2) | Payload / Data Field | Expected Status Word |
| :--- | :--- | :--- | :--- |
| **SELECT MF / Applet** | `00 A4 04 00` | AID: `A0 00 00 00 63 50 4B 43 53 2D 31 35` | `90 00` |
| **VERIFY PIN** | `00 20 00 81` | User PIN (ASCII Encoded, Zeroized after execution) | `90 00` (Success) / `63 CX` (Retries Left) |
| **GET CERTIFICATE** | `00 CB 3F FF` | Tag: `70` (X.509 Certificate Retrieval) | `90 00` / `61 XX` |
| **PSO: COMPUTE SIGNATURE** | `00 2A 9E 9A` | DigestInfo Header + 32-byte SHA-256 Document Hash | `90 00` |
| **GET RESPONSE** | `00 C0 00 00` | `Le`: Variable (Fetches remaining signature bytes) | `90 00` |

---

## 4. CCA India Rule Enforcement Matrix

| CCA Rule | Government Mandate | SecureSign Technical Implementation |
| :--- | :--- | :--- |
| **Rule 1: Key Security** | Private key must NEVER leave hardware token | On-chip RSA signing; Zero key extraction (FIPS 140-2 Level 3) |
| **Rule 2: PIN Verification** | PIN verified directly on the hardware chip | Direct `VERIFY APDU` command; RAM zeroized immediately |
| **Rule 3: Signature Standard** | PAdES / CAdES with RFC 3161 timestamp | ETSI EN 319 142-1 (PAdES-LTV) with X.509 TSA integration |
| **Rule 4: Hardware Locking** | Enforce hardware retry limits | Token hardware locks after 3 failed attempts (`SW1=0x63`) |
| **Rule 5: Audit Trail** | Maintain tamper-evident audit logs | Cryptographic audit records with IP, timestamp & cert serial |

---

## 5. Submission References
* **Production API**: `https://hackthonapp-production.up.railway.app`
* **GitHub Repository**: `https://github.com/mahankalikornepati2-netizen/hackthonapp`
* **Compiled APK**: `https://expo.dev/accounts/mahibujjipapas-team/projects/dsc-mobile-signing/builds/4384cd86-8e73-42f3-ad81-033d7bbb9d2c`
* **Word Document Dossier**: [`uploads/SecureSign_Architecture_and_Workflow_Diagrams.docx`](file:///c:/Users/ramya/Downloads/hacktiong/uploads/SecureSign_Architecture_and_Workflow_Diagrams.docx)
