import asyncio
import importlib
from pyrogram import idle

from Nexa import app, clients, ids
from Nexa.helper import join
from Nexa.modules import ALL_MODULES
from Nexa.modules.bot.start import restart_all_sessions

async def start_bot():
    # Start the main bot
    await app.start()
    print("LOG: Bot token found. Booting sᴛʀᴀɴɢᴇʀ...")

    # Dynamically import all modules
    for all_module in ALL_MODULES:
        try:
            importlib.import_module(f"Nexa.modules.{all_module}")
            print(f"✅ Successfully Imported {all_module}")
        except Exception as e:
            print(f"❌ Failed to import {all_module}: {e}")

    # Start all userbot clients
    for cli in clients:
        try:
            await cli.start()
            me = await cli.get_me()
            await join(cli)
            print(f"🔥 Started {me.first_name}")
            ids.append(me.id)
        except Exception as e:
            print(f"❌ Error starting client: {e}")

    # Restart all stored sessions
    await restart_all_sessions()
    print("✅ All sessions restarted successfully.")

    # Keep the bot running
    print("LOG: Bot is now idling...")
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())