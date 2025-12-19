import os
import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

print("🚀 Publishing project...")

# Git setup
run("git init")
run("git add .")
run('git commit -m "Auto publish" || echo "No changes to commit"')

# Check remote
remotes = subprocess.run(
    "git remote",
    shell=True,
    capture_output=True,
    text=True
).stdout

if "origin" not in remotes:
    print("🔗 Adding GitHub remote")
    run(
        f"git remote add origin https://{os.getenv('GITHUB_TOKEN')}@github.com/pranit144/trailcheak.git"
    )
else:
    print("🔁 GitHub remote already exists")

run("git branch -M main")
run("git push -u origin main")

print("✅ GitHub updated")
