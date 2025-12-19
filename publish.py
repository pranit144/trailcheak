import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

print("🚀 Publishing project...")

# 🔒 HARD-CONFIGURED REPO
GITHUB_REPO = "https://github.com/pranit144/trailcheak.git"

# Git setup
run("git init")
run("git add .")
run('git commit -m "Auto publish" || echo "No changes to commit"')

# Always ensure correct remote
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

print("✅ Successfully pushed to trailcheak 🚀")
