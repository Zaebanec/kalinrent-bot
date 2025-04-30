import os
import subprocess
from dotenv import load_dotenv

load_dotenv("t.env")

token = os.getenv("GIT_PUSH_TOKEN")
if not token:
    raise RuntimeError("GIT_PUSH_TOKEN не найден в t.env")

repo = "Zaebanec/kalinrent-bot"
remote_url = f"https://{token}@github.com/{repo}.git"

# Подменяем remote origin
subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)

# Добавляем все изменения
subprocess.run(["git", "add", "-A"])

# Проверяем — есть ли что коммитить
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
if status.stdout.strip() == "":
    print("🟡 Нет изменений для коммита.")
    exit(0)

# Коммит и пуш
subprocess.run(["git", "commit", "-m", "🤖 автопуш от кнопки"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("✅ Пуш выполнен")
