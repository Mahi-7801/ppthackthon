import urllib.request
import json

url = "https://hackthonapp-production.up.railway.app/api/otp/send-download-otp"
data = json.dumps({
    "email": "mahankalikornepati@gmail.com",
    "documentId": "ap-gov-order-104",
    "documentName": "AP_Govt_Order_MS_104.pdf"
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req, timeout=12) as resp:
    print("Railway Response:", resp.getcode(), resp.read().decode('utf-8'))
