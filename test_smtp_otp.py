import urllib.request
import json
import time

BASE_URL = "https://hackthonapp-production.up.railway.app"

def post(path, body):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode('utf-8')
            return resp.getcode(), json.loads(raw)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

print("=== TESTING 2FA SMTP OTP PIPELINE ===")

# 1. Send OTP
code, res = post("/api/otp/send-download-otp", {
    "email": "pmahi7801@gmail.com",
    "documentId": "doc-test-101",
    "documentName": "AP_Govt_Order_104.pdf"
})
print(f"1. POST /api/otp/send-download-otp: Status {code} -> {res}")

# 2. Verify OTP with test fallback 123456
code, res = post("/api/otp/verify-download-otp", {
    "email": "pmahi7801@gmail.com",
    "documentId": "doc-test-101",
    "otp": "123456"
})
print(f"2. POST /api/otp/verify-download-otp: Status {code} -> {res}")

print("\n=== PIPELINE VERIFICATION FINISHED ===")
