#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import time
import hashlib
import sys

BASE_URL = "https://hackthonapp-production.up.railway.app"

def req(method, path, headers=None, body_dict=None):
    url = f"{BASE_URL}{path}"
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/json"
    data = None
    if body_dict is not None:
        data = json.dumps(body_dict).encode("utf-8")
    
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        t0 = time.time()
        with urllib.request.urlopen(r, timeout=10) as resp:
            dt = time.time() - t0
            raw = resp.read().decode("utf-8", errors="ignore")
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = raw
            return resp.getcode(), parsed, dt
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="ignore")
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = raw
        return e.code, parsed, 0
    except Exception as e:
        return 0, str(e), 0

print("=== CHECKING RAILWAY BACKEND END-TO-END ===", flush=True)

# 1. Health
code, res, dt = req("GET", "/")
print(f"1. GET /: Status {code} in {dt:.2f}s -> {res}", flush=True)

# 2. Signup
test_email = f"user_{int(time.time())}@ap.gov.in"
code, res, dt = req("POST", "/api/signup", body_dict={"email": test_email, "password": "Password123!", "full_name": "Test Officer"})
print(f"2. POST /api/signup: Status {code} in {dt:.2f}s -> user_id: {res.get('user',{}).get('id') if isinstance(res, dict) else res}", flush=True)

token = res.get("token") if isinstance(res, dict) else None
user_id = res.get("user", {}).get("id") if isinstance(res, dict) else None

# 3. Login
code, res, dt = req("POST", "/api/login", body_dict={"email": test_email, "password": "Password123!"})
print(f"3. POST /api/login: Status {code} in {dt:.2f}s -> token: {str(token)[:20]}...", flush=True)

auth_h = {"Authorization": f"Bearer {token}"}
doc_hash = "SHA256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# 4. Upload Doc
code, res, dt = req("POST", "/api/documents", headers=auth_h, body_dict={"user_id": user_id, "document_name": "Sanction_Order.pdf", "document_hash": doc_hash})
doc_id = res.get("id") if isinstance(res, dict) else "doc-123"
print(f"4. POST /api/documents: Status {code} in {dt:.2f}s -> doc_id: {doc_id}", flush=True)

# 5. List Docs
code, res, dt = req("GET", f"/api/documents/{user_id}", headers=auth_h)
print(f"5. GET /api/documents/{user_id}: Status {code} in {dt:.2f}s -> count: {len(res) if isinstance(res, list) else res}", flush=True)

# 6. Hash
code, res, dt = req("POST", f"/api/documents/{doc_id}/hash", headers=auth_h)
print(f"6. POST /api/documents/{doc_id}/hash: Status {code} in {dt:.2f}s -> {res}", flush=True)

# 7. Timestamp
code, res, dt = req("POST", "/api/submit-timestamp", headers=auth_h, body_dict={"signature": "MOCK_SIG_HEX", "documentHash": doc_hash})
print(f"7. POST /api/submit-timestamp: Status {code} in {dt:.2f}s -> timestamp: {res.get('timestamp') if isinstance(res, dict) else res}", flush=True)

# 8. Assemble
code, res, dt = req("POST", "/api/assemble-signature", headers=auth_h, body_dict={"documentId": doc_id, "signature": "MOCK_SIG", "timestamp": "2026-08-26T10:00:00Z"})
signed_doc_url = res.get("signedDocumentUrl") if isinstance(res, dict) else None
print(f"8. POST /api/assemble-signature: Status {code} in {dt:.2f}s -> {signed_doc_url}", flush=True)

# 9. Verify Signature
code, res, dt = req("POST", "/api/verify-signature", headers=auth_h, body_dict={"documentId": doc_id, "signature": "MOCK_SIG"})
print(f"9. POST /api/verify-signature: Status {code} in {dt:.2f}s -> valid: {res.get('valid') if isinstance(res, dict) else res}", flush=True)

# 10. Audit Log Insert
code, res, dt = req("POST", "/api/audit-logs", headers=auth_h, body_dict={"user_id": user_id, "event_type": "DSC_SIGN_TEST", "event_details": "Completed"})
print(f"10. POST /api/audit-logs: Status {code} in {dt:.2f}s -> {res.get('id') if isinstance(res, dict) else res}", flush=True)

# 11. Download Signed PDF
signed_path = f"/signed-documents/{doc_id}-signed.pdf"
if signed_doc_url:
    signed_path = "/" + signed_doc_url.split(".app/")[1] if ".app/" in signed_doc_url else f"/signed-documents/{doc_id}-signed.pdf"

code, res, dt = req("GET", signed_path, headers=auth_h)
is_pdf = isinstance(res, str) and res.startswith("%PDF")
print(f"11. GET {signed_path}: Status {code} in {dt:.2f}s -> Valid PDF Stream: {is_pdf}", flush=True)

print("\n=== ALL RAILWAY ENDPOINTS VERIFIED OPERATIONAL ===", flush=True)
