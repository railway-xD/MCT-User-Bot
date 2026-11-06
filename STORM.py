from config import API_ID, API_HASH, SESSIONS
from pyrogram import Client, idle
import sys
import threading
from flask import Flask

# 1. Cloud platform health-check kosam mini Flask app
app = Flask(__name__)


@app.route("/")
def home():
  return "STORM UserBot is Active!"


def run_web():
  # Railway/Render default ga 8080 port istundi
  app.run(host="0.0.0.0", port=8080)


CLIENTS = []

for i, SESSION in enumerate(SESSIONS):
  if SESSION:
    client = Client(
        name=f"STORM{i}",
        session_string=SESSION,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=dict(root="STORM.modules"),
    )
    CLIENTS.append(client)


if __name__ == "__main__":
  # 2. Flask server ni background thread lo start chestham (Railway port error raakunda)
  web_thread = threading.Thread(target=run_web)
  web_thread.daemon = True
  web_thread.start()
  print("🌐 Flask Web Server started on port 8080")

  # 3. Telegram Clients start chestham
  for i, CLIENT in enumerate(CLIENTS):
    try:
      CLIENT.start()
      CLIENT.join_chat("STORM_CHATZ")
      print(f"ꜱᴛᴏʀᴍ ꜱᴛᴀʀᴛᴇᴅ ᴀꜱ ⚡......{i+1}")
      print(f"ʙᴏᴏᴛᴇᴅ/ꜱᴛᴀʀᴛᴇᴅ {CLIENT.me.first_name} 🎉")
    except Exception as e:
      print(e)
      print("ᴇxɪᴛɪɴɢ ᴛʜᴇ ᴘʀᴏɢʀᴀᴍ")
      sys.exit(1)

  print("ꜱᴛᴏʀᴍ ᴜꜱᴇʀ ʙᴏᴛ ɪꜱ ᴅᴇᴘʟᴏʏᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟﾙ 🌩️🥀")
  idle()
    
