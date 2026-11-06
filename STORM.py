import os
import sys
import threading
from config import API_ID, API_HASH, SESSIONS
from flask import Flask
from flask_restful import Api, Resource
from pyrogram import Client, idle

# 1. Flask Web Server Setup (from server.py)
app = Flask(__name__)
api = Api(app)


class Greeting(Resource):

  def get(self):
    return "ꜱᴛᴏʀᴍ ɪꜱ ʀᴜɴɴɪɴɢ"


api.add_resource(Greeting, "/")


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# 2. Pyrogram UserBot Clients Setup
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
  # Flask server ni background thread lo start chestham (Railway/Render health-check kosam)
  web_thread = threading.Thread(target=run_web)
  web_thread.daemon = True
  web_thread.start()
  print("🌐 Flask Web Server started successfully on port 8080!")

  # Telegram Bot Clients start chestham
  for i, CLIENT in enumerate(CLIENTS):
    try:
      CLIENT.start()
      CLIENT.join_chat("STORM_CHATZ")
      print(f"ꜱᴛᴏʀᴍ ꜱᴛᴀʀᴛᴇᴅ ᴀꜱ ⚡......{i+1}")
      print(f"ʙᴏᴏᴛᴇᴅ/ꜱᴛᴀʀᴛᴇᴅ {CLIENT.me.first_name} 🎉")
    except Exception as e:
      print(f"Error starting client {i+1}: {e}")
      sys.exit(1)

  print("ꜱᴛᴏʀᴍ ᴜꜱᴇʀ ʙᴏᴛ ɪꜱ ᴅᴇᴘʟᴏʏᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ 🌩️🥀")
  idle()
  
