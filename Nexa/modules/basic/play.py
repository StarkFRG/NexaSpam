import asyncio
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.exceptions import NoActiveGroupCall

from Nexa import CLIENTS, SUDO_USER, app
from Nexa.utils.downloader import TeleAPI


# =========================
# GLOBAL STATE
# =========================
# Per sudo:
# {
#   user_id: {
#       "vc": chat_id,
#       "queue": [file_path, ...],
#       "playing": False,
#       "client": Client
#   }
# }
VC_STATE = {}

tele = TeleAPI()

# pytgcalls per account
VCALLS = {}


# =========================
# INIT VCALLS (ON STARTUP)
# =========================
async def init_vc_clients():
    for c in CLIENTS:
        v = PyTgCalls(c)
        await v.start()
        VCALLS[c] = v


# =========================
# INTERNAL HELPERS
# =========================
async def play_next(user_id: int):
    state = VC_STATE.get(user_id)
    if not state:
        return

    if not state["queue"]:
        state["playing"] = False
        return

    file_path = state["queue"].pop(0)
    state["playing"] = True

    try:
        await VCALLS[state["client"]].join_group_call(
            state["vc"],
            AudioPiped(file_path),
        )
    except NoActiveGroupCall:
        state["playing"] = False
        raise Exception("VC is not running")


async def stop_player(user_id: int):
    state = VC_STATE.get(user_id)
    if not state:
        return
    try:
        await VCALLS[state["client"]].leave_group_call(state["vc"])
    except:
        pass
    state["queue"].clear()
    state["playing"] = False


# =========================
# JOIN VC (MULTI ACCOUNT)
# =========================
@Client.on_message(
    filters.command(["joinvc"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def joinvc_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ `.joinvc <chat_id>`")

    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❌ Invalid chat id")

    uid = message.from_user.id

    VC_STATE[uid] = {
        "vc": chat_id,
        "queue": [],
        "playing": False,
        "client": client,
    }

    await message.reply_text(
        f"✅ **VC linked**\n"
        f"👤 SUDO: `{uid}`\n"
        f"📞 VC: `{chat_id}`"
    )


# =========================
# PLAY (ANY CHAT → OWN VC)
# =========================
@Client.on_message(filters.command(["play"], ".") & filters.user(SUDO_USER))
async def play_handler(client: Client, message: Message):
    uid = message.from_user.id

    if uid not in VC_STATE:
        return await message.reply_text("❌ Use `.joinvc` first")

    if not message.reply_to_message:
        return await message.reply_text("Reply to audio / voice / video")

    media = (
        message.reply_to_message.audio
        or message.reply_to_message.voice
        or message.reply_to_message.video
    )
    if not media:
        return await message.reply_text("❌ Unsupported media")

    msg = await message.reply_text("⬇️ Downloading...")

    file_path = await tele.get_filepath(audio=media)
    ok = await tele.download({}, message, msg, file_path)
    if not ok:
        return await msg.edit("❌ Download failed")

    state = VC_STATE[uid]
    state["queue"].append(file_path)

    if not state["playing"]:
        await msg.edit("🎧 Playing...")
        await play_next(uid)
    else:
        await msg.edit(f"➕ Added to queue (`{len(state['queue'])}`)")


# =========================
# SKIP
# =========================
@Client.on_message(filters.command(["skip"], ".") & filters.user(SUDO_USER))
async def skip_handler(client: Client, message: Message):
    uid = message.from_user.id

    if uid not in VC_STATE:
        return await message.reply_text("❌ No active VC")

    await message.reply_text("⏭️ Skipping...")
    await play_next(uid)


# =========================
# STOP
# =========================
@Client.on_message(filters.command(["stop"], ".") & filters.user(SUDO_USER))
async def stop_handler(client: Client, message: Message):
    uid = message.from_user.id

    if uid not in VC_STATE:
        return await message.reply_text("❌ No active VC")

    await stop_player(uid)
    await message.reply_text("⏹️ Stopped & queue cleared")

# =========================
# LEAVE VC
# =========================
@Client.on_message(filters.command(["leavevc"], ".") & filters.user(SUDO_USER))
async def leavevc_handler(client: Client, message: Message):
    uid = message.from_user.id

    if uid not in VC_STATE:
        return await message.reply_text("❌ You are not connected to any VC")

    state = VC_STATE[uid]
    vc_chat = state["vc"]

    try:
        await stop_player(uid)
        await VCALLS[state["client"]].leave_group_call(vc_chat)
    except:
        pass

    VC_STATE.pop(uid, None)

    await message.reply_text(
        f"👋 **Left VC successfully**\n"
        f"📞 VC: `{vc_chat}`"
    )