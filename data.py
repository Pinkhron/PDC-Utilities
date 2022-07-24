import os

from dotenv import load_dotenv
from pymongo import MongoClient

# ENV & Mongo
load_dotenv()
MONGODB = os.getenv("MONGODB")
client = MongoClient(MONGODB)


class Data:
    # Bot data
    NAME = 'PDC Utilities'
    VERSION = '3.0.0a1'
    ICON = 'https://pinkhron.s3.amazonaws.com/PDC/icons/bot.png'
    OWNER_ID = 597178180176052234
    MAIN_COLOR = 0x6f0dd1

    GUILD_ID = 966934902878646323

    # Text channels
    TXT_NEWCOMERS = 992347850400858203
    TXT_GENERAL = 966934903381983324

    # Emojis
    EMOTE_MEMBER = '<:PDC_Member:992327295572377651>'
    EMOTE_SPACE = '<:space:1000187344349040732>'

    # Roles
    ROLE_MEMBER = 966940726074175498
    ROLE_TOS = 995236769077395517


class Mongo:
    DB_USER = client['user']

    CL_MEMBER = DB_USER['member']
