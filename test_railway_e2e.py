#!/usr/bin/env python3
"""
SecureSign Innovation Challenge 2026 - Comprehensive Railway Backend E2E Test Suite
Tests all 13 API endpoints on: https://app1f3f-production.up.railway.app
"""

import urllib.request
import urllib.error
import json
import time
import hashlib
import sys

BASE_URL = "https://app1f3f-production.up.railway.app"

def make_request(method, path, headers=None, body_dict=None):
    url = f"{BASE_URL}{path}"
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/json"
    headers["User-Agent"] = "SecureSign-E2E-Verifier/1.0"

    data = None
    if body_dict is not None:
        data = json.dumps(body_dict).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.getcode()
            resp_bytes = resp.read()
            try:
                resp_json = json.loads(resp_bytes.decode("utf-8"))
            except Exception:
                resp_json = resp_bytes.decode("utf-8", errors="ignore")
            return status, resp_json
    except urllib.error.HTTPError as e:
        err_bytes = e.read()
        try:
            err_json = json.loads(err_bytes.decode("utf-8"))
        except Exception:
            err_json = err_bytes.decode("utf-8", errors="ignore")
        return e.code, err_json
    except Exception as e:
        return 0, str(e)

def run_e2e_suite():
    print(f"\n🚀 Running End-to-End Verification against: {BASE_URL}\n" + "="*70)
    passed = 0
    failed = 0

    # 1. Health Check
    status, res = make_request("GET", "/")
    print(f"1. Health Check (GET /): Status {status}")
    if status == 200 and isinstance(res, dict) and res.get("status") == "ok":
        print(f"   ✔ PASS: {res}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 2. Signup
    test_email = f"officer_{int(time.time())}@ap.gov.in"
    test_pass = "SecureSign@2026"
    test_name = "Dr. K. Vijayanand, IAS"
    
    status, res = make_request("POST", "/api/signup", body_dict={
        "email": test_email,
        "password": test_pass,
        "full_name": test_name
    })
    print(f"\n2. User Registration (POST /api/signup): Status {status}")
    token = None
    user_id = None
    if status == 200 and isinstance(res, dict) and "token" in res:
        token = res["token"]
        user_id = res.get("user", {}).get("id")
        print(f"   ✔ PASS: User Created -> ID: {user_id}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 3. Login
    status, res = make_request("POST", "/api/login", body_dict={
        "email": test_email,
        "password": test_pass
    })
    print(f"\n3. User Authentication (POST /api/login): Status {status}")
    if status == 200 and isinstance(res, dict) and "token" in res:
        token = res["token"]
        user_id = res.get("user", {}).get("id", user_id)
        print(f"   ✔ PASS: JWT Token Issued -> {token[:25]}...")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    auth_headers = {"Authorization": f"Bearer {token}"}
    doc_hash = "SHA256:" + hashlib.sha256(b"Government of AP G.O. Ms 104").hexdigest()

    # 4. Upload Document
    status, res = make_request("POST", "/api/documents", headers=auth_headers, body_dict={
        "user_id": user_id,
        "document_name": "GO_Ms_104_ITE_C_Approval.pdf",
        "document_hash": doc_hash,
        "storage_path": f"{user_id}/GO_Ms_104.pdf"
    })
    print(f"\n4. Document Registration (POST /api/documents): Status {status}")
    doc_id = None
    if status == 200 and isinstance(res, dict) and "id" in res:
        doc_id = res["id"]
        print(f"   ✔ PASS: Document Created -> ID: {doc_id}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 5. Get User Documents
    status, res = make_request("GET", f"/api/documents/{user_id}", headers=auth_headers)
    print(f"\n5. List Documents by User (GET /api/documents/{user_id}): Status {status}")
    if status == 200 and isinstance(res, list):
        print(f"   ✔ PASS: Retrieved {len(res)} document(s)")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 6. Compute Document Hash
    status, res = make_request("POST", f"/api/documents/{doc_id}/hash", headers=auth_headers)
    print(f"\n6. Document Hash Calculation (POST /api/documents/{doc_id}/hash): Status {status}")
    if status == 200 and isinstance(res, dict) and "hash" in res:
        print(f"   ✔ PASS: Hash Verified -> {res['hash']}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 7. Record Hardware Signing Session
    cert_serial = "4F:8A:2D:91:00:E2:B4:7C"
    mock_signature = "30820122300d06092a864886f70d01010105000382010f00" + hashlib.sha256(b"sign_token").hexdigest() * 3
    status, res = make_request("POST", "/api/signing-sessions", headers=auth_headers, body_dict={
        "user_id": user_id,
        "document_id": doc_id,
        "certificate_serial_number": cert_serial,
        "signed_hash": doc_hash,
        "signature_blob": mock_signature,
        "timestamp_token": "TSA-RFC3161-" + str(int(time.time()))
    })
    print(f"\n7. Record Signing Session (POST /api/signing-sessions): Status {status}")
    if status == 200 and isinstance(res, dict) and "id" in res:
        session_id = res["id"]
        print(f"   ✔ PASS: Session Recorded -> ID: {session_id}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 8. Submit RFC 3161 Timestamp
    status, res = make_request("POST", "/api/submit-timestamp", headers=auth_headers, body_dict={
        "signature": mock_signature,
        "documentHash": doc_hash
    })
    print(f"\n8. RFC 3161 TSA Timestamp (POST /api/submit-timestamp): Status {status}")
    tsa_token = None
    if status == 200 and isinstance(res, dict) and "timestampToken" in res:
        tsa_token = res["timestampToken"]
        print(f"   ✔ PASS: TSA Token Issued -> {tsa_token[:30]}...")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 9. Assemble PAdES Signature
    status, res = make_request("POST", "/api/assemble-signature", headers=auth_headers, body_dict={
        "documentId": doc_id,
        "signature": mock_signature,
        "timestamp": tsa_token or str(int(time.time())),
        "certificateSerial": cert_serial
    })
    print(f"\n9. PAdES Signature Assembly (POST /api/assemble-signature): Status {status}")
    signed_url = None
    if status == 200 and isinstance(res, dict) and res.get("success") is True:
        signed_url = res.get("signedDocumentUrl")
        print(f"   ✔ PASS: PAdES Sealed -> {signed_url}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 10. Verify Digital Signature
    status, res = make_request("POST", "/api/verify-signature", headers=auth_headers, body_dict={
        "documentId": doc_id,
        "signature": mock_signature,
        "documentHash": doc_hash
    })
    print(f"\n10. Signature Verification (POST /api/verify-signature): Status {status}")
    if status == 200 and isinstance(res, dict) and res.get("valid") is True:
        print(f"   ✔ PASS: PAdES Cryptographic Verification -> {res.get('reason')}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 11. Record Audit Log
    status, res = make_request("POST", "/api/audit-logs", headers=auth_headers, body_dict={
        "user_id": user_id,
        "event_type": "HARDWARE_DSC_SIGN_COMPLETE",
        "event_details": f"Document {doc_id} signed via Type-C DSC (Serial: {cert_serial})"
    })
    print(f"\n11. Insert Audit Log (POST /api/audit-logs): Status {status}")
    if status == 200 and isinstance(res, dict) and "id" in res:
        print(f"   ✔ PASS: Audit Log Persisted -> ID: {res['id']}")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 12. List Audit Logs
    status, res = make_request("GET", f"/api/audit-logs/{user_id}", headers=auth_headers)
    print(f"\n12. Fetch Audit Trail (GET /api/audit-logs/{user_id}): Status {status}")
    if status == 200 and isinstance(res, list):
        print(f"   ✔ PASS: Retrieved {len(res)} audit record(s)")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res}")
        failed += 1

    # 13. Download Generated Signed PDF
    pdf_filename = f"{doc_id}-signed.pdf"
    status, res = make_request("GET", f"/signed-documents/{pdf_filename}", headers=auth_headers)
    print(f"\n13. Download Signed PDF (GET /signed-documents/{pdf_filename}): Status {status}")
    if status == 200 and isinstance(res, str) and res.startswith("%PDF"):
        print(f"   ✔ PASS: Valid PDF Stream Received ({len(res)} bytes)")
        passed += 1
    else:
        print(f"   ❌ FAIL: {res[:100] if isinstance(res, str) else res}")
        failed += 1

    # Summary
    print("\n" + "="*70)
    print(f"🏁 END-TO-END VERIFICATION SUMMARY:")
    print(f"   Total Endpoints Tested: 13")
    print(f"   Passed: {passed} / 13")
    print(f"   Failed: {failed} / 13")
    print(f"   Success Rate: {(passed/13)*100:.1f}%")
    print("="*70 + "\n")

    return passed == 13

if __name__ == "__main__":
    success = run_e2e_suite()
    sys.exit(0 if success else 1)
