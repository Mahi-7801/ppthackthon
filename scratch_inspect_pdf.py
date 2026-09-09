import fitz

doc = fitz.open('c:/Users/ramya/Downloads/hacktiong/hackthon_submit/SecureSign-Mobile-Digital-Signing-compressed (1).pdf')

print(f"Total pages: {len(doc)}")
for i in range(len(doc)):
    page = doc[i]
    print(f"\n--- PAGE {i+1} ---")
    text = page.get_text().strip()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines:
        print("Text preview:", " // ".join(lines[:6]))
    else:
        print("[Graphic / Image Only Slide]")
