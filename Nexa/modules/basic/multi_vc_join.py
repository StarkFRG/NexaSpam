from pyrogram import Client, filters
from pyrogram.raw.functions.phone import JoinGroupCall, LeaveGroupCall
from pyrogram.raw.types import DataJSON
from pyrogram.types import Message
from Nexa import SUDO_USER, CLIENTS
from Nexa.modules.help import add_command_help

from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.types import InputPeerChannel, InputPeerChat


async def get_group_call(client: Client, chat_id: int):
    peer = await client.resolve_peer(chat_id)

    if isinstance(peer, InputPeerChannel):
        full = (await client.invoke(GetFullChannel(channel=peer))).full_chat
    elif isinstance(peer, InputPeerChat):
        full = (await client.invoke(GetFullChat(chat_id=peer.chat_id))).full_chat
    else:
        return None

    return full.call if full else None


# =======================
# MULTI JOIN VC
# =======================
@Client.on_message(
    filters.command(["joinvc"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def multi_join_vc(client: Client, message: Message):
    args = message.command[1:]

    chat_id = message.chat.id
    if args and args[0].lstrip("-").isdigit():
        chat_id = int(args[0])
        args = args[1:]

    msg = await message.reply_text("🎧 **Joining VC with all accounts...**")

    success, failed = 0, 0

    for acc in CLIENTS:
        try:
            call = await get_group_call(acc, chat_id)
            if not call:
                failed += 1
                continue

            await acc.invoke(
                JoinGroupCall(
                    call=call,
                    params=DataJSON(data="{}"),
                    muted=False,
                    video_stopped=True,
                )
            )
            success += 1
        except Exception:
            failed += 1

    await msg.edit(
        f"✅ **Join Completed**\n"
        f"👤 Joined: `{success}`\n"
        f"❌ Failed: `{failed}`\n"
        f"📞 Chat: `{chat_id}`"
    )


# =======================
# MULTI LEAVE VC
# =======================
@Client.on_message(
    filters.command(["leavevc"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def multi_leave_vc(client: Client, message: Message):
    args = message.command[1:]

    chat_id = message.chat.id
    leave_all = False

    if args:
        if args[0].lstrip("-").isdigit():
            chat_id = int(args[0])
            args = args[1:]
        if args and args[0].lower() == "all":
            leave_all = True

    msg = await message.reply_text("👋 **Leaving VC...**")

    success, failed = 0, 0

    targets = CLIENTS if leave_all else [client]

    for acc in targets:
        try:
            call = await get_group_call(acc, chat_id)
            if not call:
                failed += 1
                continue

            await acc.invoke(LeaveGroupCall(call=call))
            success += 1
        except Exception:
            failed += 1

    await msg.edit(
        f"👋 **Leave Completed**\n"
        f"👤 Left: `{success}`\n"
        f"❌ Failed: `{failed}`\n"
        f"📞 Chat: `{chat_id}`"
    )


add_command_help(
    "multivc",
    [
        ["joinvc <chat_id>", "All userbot accounts join VC"],
        ["leavevc all", "All userbot accounts leave VC"],
        ["leavevc", "Current userbot leaves VC"],
    ],
)