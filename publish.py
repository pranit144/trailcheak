#!/usr/bin/env python3
"""
publish.py
- pushes the current folder to GitHub (pranit144/trailcheak)
- publishes the folder to Hugging Face as a Docker Space (pranit144/trailcheak)
- excludes .git and other forbidden files from the HF upload
"""

import os
import subprocess
import sys
from huggingface_hub import create_repo, upload_folder
from huggingface_hub.utils._errors import HfHubHTTPError

# -------------------------
# CONFIG - edit only these
# -------------------------
GITHUB_REPO = "https://github.com/pranit144/trailcheak.git"
HF_USERNAME = "pranit144"
HF_REPO_NAME = "trailcheak"
HF_REPO_ID = f"{HF_USERNAME}/{HF_REPO_NAME}"
HF_SPACE_SDK = "docker"      # your space is a Docker Space
BRANCH = "main"
# -------------------------

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("❌ ERROR: HF_TOKEN environment variable is not set.")
    print("Set it with: setx HF_TOKEN \"hf_xxx\"  (then restart your terminal)")
    sys.exit(1)

def run(cmd, check=True):
    """Run a shell command (prints it)."""
    print(f"> {cmd}")
    return subprocess.run(cmd, shell=True, check=check)

def run_safe(cmd):
    """Run a shell command but don't raise on failure."""
    try:
        return run(cmd, check=True)
    except subprocess.CalledProcessError:
        return None

# -------------------------
# GIT / GitHub section
# -------------------------
print("🚀 Publishing project...")

print("🔧 GitHub: preparing repo")
run_safe("git init")
run(f"git checkout -B {BRANCH}")
run("git add .")
# commit if there are changes, otherwise skip (non-fatal)
run_safe('git commit -m "Auto publish"')

print("🔗 GitHub: ensuring correct remote")
# remove any existing origin (safe) then add correct remote
run_safe("git remote remove origin")
run(f"git remote add origin {GITHUB_REPO}")

# push (force to ensure remote matches local; safe because this is your repo)
run(f"git push -u origin {BRANCH} --force")

print("✅ GitHub push successful")
print(f"🔗 GitHub: {GITHUB_REPO}")

# -------------------------
# Hugging Face section
# -------------------------
print("🤗 Hugging Face: publishing Docker Space")

# Ensure repo exists (create if not)
try:
    create_repo(
        repo_id=HF_REPO_ID,
        repo_type="space",
        space_sdk=HF_SPACE_SDK,
        token=HF_TOKEN,
        exist_ok=True,
        private=False,
    )
    print("✅ Hugging Face Space exists (or was created).")
except Exception as e:
    # create_repo may raise for many reasons; print but continue to upload attempt
    print("⚠️ Warning while creating/ensuring HF Space:", str(e))

# upload_folder: exclude .git and other local/forbidden files
IGNORE_PATTERNS = [
    ".git/**",        # everything under .git
    ".git",           # just in case
    ".github/**",
    ".venv/**",
    "venv/**",
    "__pycache__/**",
    "*.pyc",
    "node_modules/**",
    ".env",
    ".DS_Store",
]

try:
    upload_folder(
        repo_id=HF_REPO_ID,
        folder_path=".",
        repo_type="space",
        token=HF_TOKEN,
        commit_message="Auto publish from script",
        ignore_patterns=IGNORE_PATTERNS,
    )
    print("✅ Hugging Face Space updated successfully!")
    print(f"🔗 HF Space: https://huggingface.co/spaces/{HF_REPO_ID}")
except HfHubHTTPError as e:
    print("❌ Hugging Face upload failed with HTTP error:")
    print(str(e))
    print("\nCommon causes:")
    print("- Forbidden filenames (make sure .git is excluded).")
    print("- Token missing or insufficient scope (need write perms).")
    print("- Very large files / LFS issues.")
    print("\nWhat you can do now:")
    print("1) Verify HF_TOKEN: it must have write permissions.")
    print("2) Make sure .git/ is present locally and NOT uploaded (script excludes it).")
    print("3) If the error mentions a specific filename, remove it or add it to IGNORE_PATTERNS.")
    sys.exit(1)
except Exception as e:
    print("❌ Unexpected error while uploading to Hugging Face:")
    print(str(e))
    sys.exit(1)

print("🎉 ALL DONE!")
