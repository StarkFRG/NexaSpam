import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")


API_ID = int(getenv("API_ID", "22657083")) #optional
API_HASH = getenv("API_HASH", "d6186691704bd901bdab275ceaab88f3") #optional

OWNER_ID = int(getenv("OWNER_ID","1118345061"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "8553815122").split()))
SUDOS = list(map(int, getenv("SUDO_USERS", "8553815122").split()))
DEVS = list(map(int, getenv("DEVS", "8553815122").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://onyxcoders:aH8lNcURcuDmkL7D@cluster0.1ojawuj.mongodb.net/?appName=Cluster0")
BOT_TOKEN = getenv("BOT_TOKEN", "8511029028:AAHvJwW_gxUO34hV543op_VaTgEKuZsUaNA")
ALIVE_PIC = getenv("ALIVE_PIC", 'https://files.catbox.moe/9ux4mb.jpg')
ALIVE_TEXT = getenv("ALIVE_TEXT")
PM_LOGGER = getenv("PM_LOGGER")
LOG_GROUP = getenv("LOG_GROUP", "-1003739009228")
GIT_TOKEN = getenv("GIT_TOKEN") #personal access token
REPO_URL = getenv("REPO_URL", "https://github.com/StarkFRG/NexaSpam")
BRANCH = getenv("BRANCH", "main") #don't change
 
STRING_SESSION1 = getenv("STRING_SESSION1", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")
STRING_SESSION6 = getenv("STRING_SESSION6", "")
STRING_SESSION7 = getenv("STRING_SESSION7", "")
STRING_SESSION8 = getenv("STRING_SESSION8", "")
STRING_SESSION9 = getenv("STRING_SESSION9", "")
STRING_SESSION10 = getenv("STRING_SESSION10", "")
