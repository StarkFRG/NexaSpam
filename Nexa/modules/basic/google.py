import requests
from bs4 import BeautifulSoup
from googlesearch import search
from pyrogram import Client, filters
from pyrogram.types import Message

from Nexa.helper.basic import edit_or_reply
from Nexa.modules.help import add_command_help


def googlesearch(query):
    results = {}
    count = 1
    for url in search(query, tld="co.in", num=10, stop=10, pause=2):
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.find("title")
            site_title = title_tag.get_text().strip() if title_tag else "No Title"

            meta_tags = soup.find_all("meta")
            meta_desc = [
                meta.attrs["content"]
                for meta in meta_tags
                if "name" in meta.attrs and meta.attrs["name"].lower() == "description"
            ]

            results[count] = {
                "title": site_title,
                "metadata": meta_desc,
                "url": url,
            }
            count += 1
        except Exception:
            continue  
    return results


@Client.on_message(filters.command(["gs", "google"], ".") & filters.me)
async def gs(client: Client, message: Message):
    man = await edit_or_reply(message, "`Searching Google...`")
    msg_text = message.text.strip()

    if " " not in msg_text:
        return await man.edit("**Please provide a search query.**")

    query = msg_text.split(" ", 1)[1]
    results = googlesearch(query)

    if not results:
        return await man.edit("**No results found.**")

    response_msg = ""
    for i, result in results.items():
        title = result.get("title", "No Title")
        url = result.get("url", "#")
        meta = result.get("metadata", ["No description available."])[0]
        meta = (meta[:200] + "...") if len(meta) > 200 else meta
        response_msg += f"[{title}]({url})\n{meta}\n\n"

    await man.edit(response_msg, disable_web_page_preview=True)

add_command_help(
    "google",
    [
        ["google <query>", "Searches Google and returns the top results with titles and descriptions."]
    ],
)
