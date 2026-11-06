import os
import threading
from config import API_ID, API_HASH, SESSIONS
from flask import Flask
from pyrogram import Client, idle

app = Flask(__name__)


@app.route("/")
def home():
  return "STORM UserBot is Active!"


def run_web():
  # Railway/Render dynamic PORT provide chesthe adhi tisukuntundhi, leda default 8080
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


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
  web_thread = threading.Thread(target=run_web)
  web_thread.daemon = True
  web_thread.start()

  for i, CLIENT in enumerate(CLIENTS):
    try:
      CLIENT.start()
      CLIENT.join_chat("STORM_CHATZ")
      print(f"ꜱᴛᴏʀᴍ ꜱᴛᴀʀᴛᴇᴅ ᴀꜱ ⚡......{i+1}")
      print(f"ʙᴏᴏᴛᴇᴅ/ꜱᴛᴀʀᴛᴇᴅ {CLIENT.me.first_name} 🎉")
    except Exception as e:
      print(f"Error starting client {i+1}: {e}")

  print("ꜱᴛᴏʀᴍ ᴜꜱᴇʀ ʙᴏᴛ ɪꜱ ᴅᴇᴘʟᴏʏᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ 🌩️🥀")
  idle()
  
