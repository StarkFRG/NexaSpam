import os
from Nexa.modules.help import add_command_help
from pyrogram import Client, filters

COMMANDS = ["op", "wow", "nice", "super"]

@Client.on_message(filters.command(COMMANDS, prefixes=["", "."]) & filters.private & filters.me)
async def self_media(client, message):
    try:
        replied = message.reply_to_message
        if not replied:
            return await message.reply("Reply to a self-destruct photo/video to save it.")
        
        if not (replied.photo or replied.video):
            return await message.reply("Only self-destruct photo or video can be saved.")

        # Download and send to Saved Messages
        location = await client.download_media(replied)
        await client.send_document("me", location, caption="Saved self-destruct media.")
        os.remove(location)
        await message.reply("😻 hmm")
    except Exception as e:
        await message.reply(f"Error: `{e}`")

add_command_help(
    "destruct",
    [
        [".op", "Reply to a self-destruct photo or video to save it to your Saved Messages."],
        ["🌿 More Commands", "😋🥰, wow, super, 😋😍"],
    ],
)
