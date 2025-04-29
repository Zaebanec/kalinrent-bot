from flask import Flask, request
import subprocess
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(filename='webhook.log', level=logging.INFO)

@app.route("/update", methods=["POST"])
def update():
    logging.info(f"{datetime.now()} — Webhook received")

    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        subprocess.run(["pkill", "-f", "main.py"])
        subprocess.Popen(["nohup", "python3", "main.py", "&"])
        logging.info("Bot updated and restarted successfully")
        return "Bot updated", 200
    except Exception as e:
        logging.error(f"Update failed: {e}")
        return "Update failed", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

