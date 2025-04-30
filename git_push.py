
import os
import subprocess
from dotenv import load_dotenv

load_dotenv("t.env")

token = os.getenv("GIT_PUSH_TOKEN")
if not token:
    raise RuntimeError("GIT_PUSH_TOKEN не найден в t.env")

repo = "Zaebanec/kalinrent-bot"
remote_url = f"https://{token}@github.com/{repo}.git"

# Устанавливаем origin
subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)

# Добавляем все изменения
subprocess.run(["git", "add", "-A"])

# Проверяем — есть ли что коммитить (только реальные изменения)
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
lines = status.stdout.strip().splitlines()
real_changes = [line for line in lines if not line.endswith(("nohup.out", "webhook.log", ".DS_Store"))]

if not real_changes:
    exit(2)

# Коммит и пуш
subprocess.run(["git", "commit", "-m", "🤖 автопуш от кнопки"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

exit(0)
