from Nexa.modules.bot.start import restart_all_sessions
import asyncio
import importlib
from pyrogram import Client, idle
from Nexa.helper import join
from Nexa.modules import ALL_MODULES
from Nexa import clients, app, ids

async def start_bot():
    await app.start()
    print("LOG: Founded Bot token. Booting sᴛʀᴀɴɢᴇʀ.")

    # Import modules dynamically
    for all_module in ALL_MODULES:
        importlib.import_module("Nexa.modules" + all_module)
        print(f"Successfully Imported {all_module} 💥")

    # Start all clients
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"Error starting client: {e}")

    # Restart all stored sessions before idling
    await restart_all_sessions()

    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
