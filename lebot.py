import time
import twitchio
import asyncio
from twitchio import PartialUser
from twitchio.ext import commands,pubsub
import random
import aiofiles as aiof
import inspect
import json

def prepare(bot):
    bot.add_cog(NewCog(bot))


CONFIG_FILE = "config.json"
with open(CONFIG_FILE, "r") as configur:
          data = json.load(configur)
          oauthtoken = data["oauthkey"]
          modtoken = data["modoauthkey"]
          userID = data["userID"]
          channel = data["channel"]
          moderatorID = data["moderatorID"]
          eventname= data["EventName"]


users_channel_id = userID
users_oauth_token = modtoken
class NewCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.pubsub = pubsub.PubSubPool(bot)


    @commands.Cog.event()
    async def event_ready(self):
        topics = [
        pubsub.channel_points(users_oauth_token)[users_channel_id]]
        await self.bot.pubsub.subscribe_topics(topics)
    
    async def event_pubsub_channel_points2(self, event:pubsub.PubSubChannelPointsMessage ):
        broadcaster = (await self.bot.fetch_users(ids=[event.channel_id]))[0]
        channel = self.bot.get_channel(channel)
        print(event.user.name)
        print(event.user.id)
        print(event.reward.title)
        redeemer = event.user.name
        if event.reward.title == eventname:
         CONFIG_FILE = "config.json"

         with open(CONFIG_FILE, "r") as configur:
          data = json.load(configur)
          data["wheelspun"] = "False"
          with open(CONFIG_FILE, mode='w') as handle:
           json.dump(data, handle, indent=4)
         while data["wheelspun"] == "False":  
          await asyncio.sleep(.1)
          with open(CONFIG_FILE, "r") as configur:
           data = json.load(configur)
         if data["wheelspun"] == "True":
             PRIZE = data["latestprize"]

             if PRIZE == "1 Minute Timeout":
              await broadcaster.timeout_user(token=oauthtoken, moderator_id=moderatorID, user_id=event.user.id, duration=60, reason="u lost lol")
              await channel.send(f'{redeemer} you got a 1 minute timeout  ')
             elif PRIZE == "3 MINUTE TO":
               await broadcaster.timeout_user(token=oauthtoken, moderator_id=moderatorID, user_id=event.user.id, duration=180, reason="u lost lol")
               await channel.send(f'{redeemer} you got a 3 minute timeout lol')
             elif PRIZE == "5 MINUTE TO":
              await broadcaster.timeout_user(token=oauthtoken, moderator_id=moderatorID, user_id=event.user.id, duration=300, reason="u lost lol")
              await channel.send(f'{redeemer} you got a 5 minute timeout fuckin dumbass')
             elif PRIZE =="SUB":
               await channel.send(f'{redeemer} YOU WON A FREE SUB PagMan')      
             elif PRIZE == "EMOTE":
                 await channel.send(f'{redeemer} you get to make a new sub emote :)')
             elif PRIZE =="VIP":
               with open(CONFIG_FILE,'r') as f:
                 data = json.load(f)
                 pv1 = int(data["previousvipid"])
               await channel.send(f'{redeemer} YOU WON VIP JermaAward')  
               await asyncio.sleep(.13)
               await channel.send(f'{redeemer} YOU WON VIP JermaAward')  
               await asyncio.sleep(.13)
               await channel.send(f'{redeemer} YOU WON VIP JermaAward')  
               await asyncio.sleep(.13)                 
               print(pv1)
               await broadcaster.add_channel_vip(token=oauthtoken,user_id=event.user.id)
               await broadcaster.remove_channel_vip(token=oauthtoken,user_id=pv1)
               data["previousvipid"] = f"{event.user.id}"
               with open(CONFIG_FILE, mode='w') as handle:
                    json.dump(data, handle, indent=4)
             elif PRIZE =="Gifted Sub":
               await channel.send(f'{redeemer} you get to make a tweet, be funny or i will kill you Erm')

      # pass # do stuff on channel point redemptions
        print("recieved channelpoint reward")
    @commands.Cog.event()
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        await self.event_pubsub_channel_points2(event)
    
