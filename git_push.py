import os
import subprocess
from dotenv import load_dotenv

load_dotenv("t.env")

token = os.getenv("GIT_PUSH_TOKEN")
if not token:
    raise RuntimeError("GIT_PUSH_TOKEN не найден в t.env")

repo = "Zaebanec/kalinrent-bot"
remote_url = f"https://{token}@github.com/{repo}.git"

subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)
subprocess.run(["git", "add", "-A"])

status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
if status.stdout.strip() == "":
    exit(2)  # специальных код, если нечего пушить

subprocess.run(["git", "commit", "-m", "🤖 автопуш от кнопки"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

exit(0)
