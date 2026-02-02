from pyrogram import Client
from config import (
    API_ID,
    API_HASH,
    SUDO_USERS,
    OWNER_ID,
    BOT_TOKEN,
    STRING_SESSION1,
    STRING_SESSION2,
    STRING_SESSION3,
    STRING_SESSION4,
    STRING_SESSION5,
    STRING_SESSION6,
    STRING_SESSION7,
    STRING_SESSION8,
    STRING_SESSION9,
    STRING_SESSION10,
)
from datetime import datetime
import time

# --------------------------
# STARTUP TIME
# --------------------------
StartTime = time.time()
START_TIME = datetime.now()

# --------------------------
# GLOBALS
# --------------------------
CMD_HELP = {}
SUDO_USER = SUDO_USERS
clients = []  # list of all userbot clients
ids = []      # list of userbot ids

# Add owner to sudo users
if OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)

# --------------------------
# API ID & HASH defaults
# --------------------------
API_ID = API_ID or 22657083
API_HASH = API_HASH or "d6186691704bd901bdab275ceaab88f3"

if not BOT_TOKEN:
    print("⚠️ WARNING: BOT TOKEN NOT FOUND. Add it to config.")

# --------------------------
# Main bot
# --------------------------
app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Nexa/modules/bot"),
    in_memory=True,
)

# --------------------------
# Userbot sessions
# --------------------------
SESSION_LIST = [
    STRING_SESSION1, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4, STRING_SESSION5,
    STRING_SESSION6, STRING_SESSION7, STRING_SESSION8, STRING_SESSION9, STRING_SESSION10
]

SESSION_NAMES = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"
]

for i, session_str in enumerate(SESSION_LIST):
    if session_str:
        print(f"Client {i+1}: Found.. Starting.. 📳")
        client = Client(
            name=SESSION_NAMES[i],
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_str,
            plugins=dict(root="Nexa/modules")
        )
        clients.append(client)