import json

# JSON

with open('./json/server.json') as s:
    server = json.load(s)

with open('./json/responses.json') as res:
    responses = json.load(res)

with open('./json/assets.json') as a:
    assets = json.load(a)


class Data:
    GUILD_ID = server['guild_id']
    VC_GLOBAL = server['channels']['member']['vc_global']
    ROLE_ORGANIZER = server['roles']['organizer']

    VERSION = assets['version']
    LOGO_BOT = assets['icons']['bot']
    LOGO_DEFAULT = assets['icons']['default']

    SHIP_LOAD = responses['ship_load']
    BALL_RESPONSE = responses['8ball_response']
    FOOTER = responses['footer']
