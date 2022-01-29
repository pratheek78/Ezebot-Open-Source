import discord, pymongo, os

from discord.ext import commands
from dotenv import load_dotenv

from DiscordBot import client

"""Optimise Database usage by removing server data when the bot leaves that server"""

# Mongo variables
load_dotenv()
MONGOCONN = os.getenv('Mongo_conn')
cl = pymongo.MongoClient(MONGOCONN)
mdb = cl['Ezebot']

# These are the collections in use
modcoll = mdb['Modlogging'] #Moderation collection
prefixcoll = mdb['prefix'] #prefix collection
msgcoll = mdb['ui_messages'] #Messages collection


class db_optimise(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        modcoll.delete_many({'guild_id': guild.id})
        msgcoll.delete_many({'guild_id': guild.id})
        prefixcoll.delete_many({'guild_id': guild.id})
        print(f'Bot was removed from guild- {guild.name}. All guild-related data has been removed.')
        await guild.owner.send(f'Ezebot has been removed from {guild.name}. All data of this guild(prefix, cases, message logs) have been removed from our database')

def setup(client):
    client.add_cog(db_optimise(client))

