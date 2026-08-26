#!/usr/bin/env python3
"""
Create a complete safe backup of all existing mobile and backend files
before applying the strict hybrid production upgrade.
"""

import os
import shutil
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIMESTAMP = time.strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = os.path.join(BASE_DIR, f"backup_hackathon_{TIMESTAMP}")

os.makedirs(BACKUP_DIR, exist_ok=True)

# Files to backup
FILES_TO_BACKUP = [
    os.path.join(BASE_DIR, "mobile", "app", "android", "app", "src", "main", "java", "com", "dscsigning", "DSCSigningModule.kt"),
    os.path.join(BASE_DIR, "mobile", "app", "android", "app", "src", "main", "java", "com", "dscsigning", "CcidTransport.kt"),
    os.path.join(BASE_DIR, "mobile", "app", "android", "app", "src", "main", "java", "com", "dscsigning", "P11Wrapper.kt"),
    os.path.join(BASE_DIR, "mobile", "app", "android", "app", "src", "main", "java", "com", "dscsigning", "DSCUsbManager.kt"),
    os.path.join(BASE_DIR, "mobile", "app", "src", "services", "DSCService.ts"),
    os.path.join(BASE_DIR, "mobile", "app", "src", "services", "BackendService.ts"),
    os.path.join(BASE_DIR, "backend", "server.js"),
]

print(f"Creating backup in: {BACKUP_DIR}\n")
for f in FILES_TO_BACKUP:
    if os.path.exists(f):
        rel = os.path.relpath(f, BASE_DIR)
        dest = os.path.join(BACKUP_DIR, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(f, dest)
        print(f"  ✔ Backed up: {rel}")
    else:
        print(f"  ⚠️ File not found: {f}")

print("\n--- BACKUP COMPLETED SAFELY ---")
