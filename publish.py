import subprocess
import os
from huggingface_hub import create_repo, upload_folder

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

print("🚀 Publishing project...")

# =======================
# GitHub CONFIG
# =======================
GITHUB_REPO = "https://github.com/pranit144/trailcheak.git"

run("git init")
run("git add .")
run('git commit -m "Auto publish" || echo "No changes to commit"')

print("🔗 Ensuring GitHub remote is trailcheak")

remotes = subprocess.run(
    "git remote",
    shell=True,
    capture_output=True,
    text=True
).stdout

if "origin" not in remotes:
    run(f"git remote add origin {GITHUB_REPO}")
else:
    run(f"git remote set-url origin {GITHUB_REPO}")

run("git branch -M main")
run("git push -u origin main")

print("✅ GitHub updated")

# =======================
# Hugging Face CONFIG
# =======================
HF_USERNAME = "pranit144"   # 👈 CHANGE THIS
HF_REPO_NAME = "trailcheak"
HF_REPO_TYPE = "space"             # "space" or "model"

print("🤗 Publishing to Hugging Face...")

create_repo(
    repo_id=f"{HF_USERNAME}/{HF_REPO_NAME}",
    repo_type=HF_REPO_TYPE,
    token=os.getenv("HF_TOKEN"),
    exist_ok=True
)

upload_folder(
    folder_path=".",
    repo_id=f"{HF_USERNAME}/{HF_REPO_NAME}",
    repo_type=HF_REPO_TYPE,
    token=os.getenv("HF_TOKEN")
)

print("✅ Hugging Face updated 🚀")
print("🎉 ALL DONE!")
