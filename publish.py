import os
import subprocess
from huggingface_hub import create_repo, upload_folder

# ------------------------
# Helpers
# ------------------------
def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

print("🚀 Publishing project...")

# ========================
# CONFIG
# ========================
GITHUB_REPO = "https://github.com/pranit144/trailcheak.git"

HF_USERNAME = "pranit144"
HF_REPO_NAME = "trailcheak"
HF_REPO_TYPE = "space"
HF_SPACE_SDK = "docker"   # IMPORTANT: matches your Docker Space

# ========================
# GITHUB PUBLISH
# ========================
print("🔧 GitHub: preparing repo")

run("git init")
run("git add .")
run('git commit -m "Auto publish" || echo "No changes to commit"')

remotes = subprocess.run(
    "git remote",
    shell=True,
    capture_output=True,
    text=True
).stdout

print("🔗 GitHub: ensuring correct remote")

if "origin" not in remotes:
    run(f"git remote add origin {GITHUB_REPO}")
else:
    run(f"git remote set-url origin {GITHUB_REPO}")

run("git branch -M main")
run("git push -u origin main")

print("✅ GitHub push successful")

# ========================
# HUGGING FACE PUBLISH
# ========================
print("🤗 Hugging Face: publishing Docker Space")

if not os.getenv("HF_TOKEN"):
    raise RuntimeError("❌ HF_TOKEN not found in environment variables")

create_repo(
    repo_id=f"{HF_USERNAME}/{HF_REPO_NAME}",
    repo_type=HF_REPO_TYPE,
    space_sdk=HF_SPACE_SDK,
    token=os.getenv("HF_TOKEN"),
    exist_ok=True
)

upload_folder(
    folder_path=".",
    repo_id=f"{HF_USERNAME}/{HF_REPO_NAME}",
    repo_type=HF_REPO_TYPE,
    token=os.getenv("HF_TOKEN"),
    ignore_patterns=[".git", ".venv", "__pycache__"]
)

print("✅ Hugging Face Space updated")

print("🎉 ALL DONE!")
print("🔗 GitHub: https://github.com/pranit144/trailcheak")
print("🤗 HF Space: https://huggingface.co/spaces/pranit144/trailcheak")
