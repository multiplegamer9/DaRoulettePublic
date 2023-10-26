import twitchio
from twitchio.ext import commands
import json

CONFIG_FILE = "config.json"
with open(CONFIG_FILE, "r") as configur:
          data = json.load(configur)
          oauthtoken = data["oauthkey"]
          modtoken = data["xaltoken"]
          userID = data["userID"]
          channel = data["channel"]
users_oauth_token = modtoken

my_token = oauthtoken
xalbot_token = modtoken

bot = commands.Bot(my_token, prefix="!", initial_channels=[channel])

@bot.event()
async def event_ready():
    print(f"Ready | {bot.nick}")
initial_extensions = ["lebot"]
for extension in initial_extensions:
    bot.load_module(extension)
bot.run()
