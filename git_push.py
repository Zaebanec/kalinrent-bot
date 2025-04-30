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

# Проверка: есть ли что коммитить?
check = subprocess.run(["git", "diff", "--cached", "--quiet"])
if check.returncode == 1:
    subprocess.run(["git", "commit", "-m", "🤖 автопуш от кнопки"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    exit(0)
else:
    # индекс пуст — нечего пушить
    exit(2)
