import os
import subprocess

GITHUB_USERNAME = "pranit144"
HF_USERNAME = "pranit144"
PROJECT_NAME = "weather-app"
HF_TYPE = "space"  # "model" or "space"

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

print("🚀 Publishing project...")

# ------------------ GitHub ------------------
run("git init")
run("git add .")
run('git commit -m "Initial commit"')

run(
    f"git remote add origin https://{os.getenv('GITHUB_TOKEN')}@github.com/{GITHUB_USERNAME}/{PROJECT_NAME}.git"
)
run("git branch -M main")
run("git push -u origin main")

print("✅ Pushed to GitHub")

# ------------------ Hugging Face ------------------
run("pip install -q huggingface_hub")

from huggingface_hub import create_repo, upload_folder

repo_id = f"{HF_USERNAME}/{PROJECT_NAME}"

create_repo(
    repo_id=repo_id,
    token=os.getenv("HF_TOKEN"),
    repo_type=HF_TYPE,
    exist_ok=True
)

upload_folder(
    repo_id=repo_id,
    folder_path=".",
    token=os.getenv("HF_TOKEN"),
    repo_type=HF_TYPE
)

print("✅ Published to Hugging Face")
print("🎉 DONE!")
