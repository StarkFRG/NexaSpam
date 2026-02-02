import asyncio
import os
import time
from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Voice

from Nexa import app
from Nexa.utils.formatters import (
    check_duration,
    convert_bytes,
    get_readable_time,
    seconds_to_min,
)


class TeleAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.sleep = 5

    # -----------------------
    # Split long text for Telegram messages
    # -----------------------
    async def send_split_text(self, message, string):
        n = self.chars_limit
        out = [(string[i : i + n]) for i in range(0, len(string), n)]
        for j, x in enumerate(out):
            if j <= 2:
                await message.reply_text(x, disable_web_page_preview=True)
        return True

    # -----------------------
    # Get file name
    # -----------------------
    async def get_filename(self, file, audio: Union[bool, str] = None):
        try:
            file_name = file.file_name
            if not file_name:
                file_name = "ᴛᴇʟᴇɢʀᴀᴍ ᴀᴜᴅɪᴏ" if audio else "ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ"
        except Exception:
            file_name = "ᴛᴇʟᴇɢʀᴀᴍ ᴀᴜᴅɪᴏ" if audio else "ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ"
        return file_name

    # -----------------------
    # Get duration for downloaded file
    # -----------------------
    async def get_duration(self, filex, file_path):
        try:
            dur = seconds_to_min(filex.duration)
        except:
            try:
                dur_sec = await asyncio.get_event_loop().run_in_executor(
                    None, check_duration, file_path
                )
                dur = seconds_to_min(dur_sec)
            except:
                dur = "Unknown"
        return dur

    # -----------------------
    # Filepath generator
    # -----------------------
    async def get_filepath(
        self,
        audio: Union[bool, str] = None,
        video: Union[bool, str] = None,
    ):
        os.makedirs("downloads", exist_ok=True)
        if audio:
            try:
                ext = (
                    audio.file_name.split(".")[-1]
                    if not isinstance(audio, Voice)
                    else "ogg"
                )
            except Exception:
                ext = "ogg"
            file_name = f"{audio.file_unique_id}.{ext}"

        elif video:
            try:
                ext = video.file_name.split(".")[-1]
            except Exception:
                ext = "mp4"
            file_name = f"{video.file_unique_id}.{ext}"

        else:
            return None

        return os.path.join(os.path.realpath("downloads"), file_name)

    # -----------------------
    # Download media with progress
    # -----------------------
    async def download(self, _, message, mystic, fname):
        lower = [0, 8, 17, 38, 64, 77, 96]
        higher = [5, 10, 20, 40, 66, 80, 99]
        checker = [5, 10, 20, 40, 66, 80, 99]
        speed_counter = {}

        if os.path.exists(fname):
            return True

        async def down_load():
            async def progress(current, total):
                if current == total:
                    return

                start_time = speed_counter.get(message.id)
                if not start_time:
                    return

                elapsed = time.time() - start_time
                if elapsed <= 0:
                    return

                percentage = int((current * 100) / total)
                speed = convert_bytes(current / elapsed)
                eta = get_readable_time(int((total - current) / (current / elapsed)))
                completed = convert_bytes(current)
                total_size = convert_bytes(total)

                upl = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ᴄᴀɴᴄᴇʟ", callback_data="stop_downloading")]]
                )

                for i in range(7):
                    if lower[i] < percentage <= higher[i] and checker[i] != 100:
                        try:
                            await mystic.edit_text(
                                _["tg_1"].format(
                                    app.mention,
                                    total_size,
                                    completed,
                                    percentage,
                                    speed,
                                    eta,
                                ),
                                reply_markup=upl,
                            )
                            checker[i] = 100
                        except:
                            pass

            speed_counter[message.id] = time.time()
            try:
                await app.download_media(
                    message.reply_to_message,
                    file_name=fname,
                    progress=progress,
                )
                await mystic.edit_text(_["tg_2"].format("Completed"))
            except Exception:
                await mystic.edit_text(_["tg_3"])

        task = asyncio.create_task(down_load())
        try:
            config.lyrical[mystic.id] = task
        except:
            config.lyrical = {mystic.id: task}
        await task
        config.lyrical.pop(mystic.id, None)
        return True