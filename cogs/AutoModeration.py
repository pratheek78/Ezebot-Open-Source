import discord
import pymongo


from discord.ext import commands

cl = pymongo.MongoClient("")
db = cl['Ezebot']
acoll = db['automod']


class AutoMod(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command() #NEEDS TON OF WORK, PLEASE DO NOT USE THIS IT IS COMPLETELY FUCKED UP
    @commands.has_permissions(administrator = True)
    async def automod(self, ctx):
        result = acoll.find_one({'guild_id': ctx.message.guild.id})

        if result is None:
            post = {'guild_id': ctx.message.guild.id,
                    'toggle': True}
            acoll.insert_one(post)
            await ctx.send('Automod is now turned on')

        if result is not None:
            result = result.get('toggle')

            if result == True:
                acoll.delete_one
                await ctx.send('automod is now off')



def setup(client):
    client.add_cog(AutoMod(client))