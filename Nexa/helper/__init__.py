import os
import sys
from pyrogram import Client



def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Nexa"])

async def join(client):
    try:
        await client.join_chat("urstarkz")
    except BaseException:
        pass
