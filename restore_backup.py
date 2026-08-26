#!/usr/bin/env python3
"""
Emergency Restore Script
Instantly restores all original hackathon files from the safe backup folder.
"""

import os
import shutil
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Find the latest backup directory
backup_folders = sorted(glob.glob(os.path.join(BASE_DIR, "backup_hackathon_*")), reverse=True)

if not backup_folders:
    print("❌ No backup directory found!")
    exit(1)

LATEST_BACKUP = backup_folders[0]
print(f"Restoring from safe backup: {LATEST_BACKUP}\n")

for root, dirs, files in os.walk(LATEST_BACKUP):
    for f in files:
        src = os.path.join(root, f)
        rel = os.path.relpath(src, LATEST_BACKUP)
        dest = os.path.join(BASE_DIR, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  ✔ Restored: {rel}")

print("\n--- ALL ORIGINAL FILES RESTORED SUCCESSFULLY ---")
