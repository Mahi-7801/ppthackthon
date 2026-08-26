import urllib.request

url = "https://app1f3f-production.up.railway.app/signed-documents/f5ddd23b-a08b-479c-ba05-47e939d1e5c8-signed-1787721069899.pdf"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
        print(f"Status: {resp.getcode()}, Length: {len(content)} bytes, StartsWith: {content[:10]}")
except Exception as e:
    print(f"Error: {e}")
