import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="t.env")

TOKEN = os.getenv("BOT_TOKEN")
