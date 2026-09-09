import fitz

doc = fitz.open('c:/Users/ramya/Downloads/hacktiong/hackthon_submit/SecureSign-Mobile-Digital-Signing-compressed (1).pdf')

for i in range(len(doc)):
    page = doc[i]
    print(f"=== Page {i+1} ===")
    print("Text content:\n", page.get_text())
