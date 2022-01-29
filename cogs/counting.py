import discord, pymongo, os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
MONGOCONN = os.getenv('Mongo_conn')
cl = pymongo.MongoClient(MONGOCONN)
mdb = cl['Ezebot']
countcoll = mdb['counting']

cares = (" ✅ When a message is deleted\n"
         " ✅ When a message is edited\n"
         " ✅ When a fake reaction is added\n"
         " ❌ Non-counting messages\n"
         " ❌ Trailing text after numbers")

def clean(content):
    number = ""
    for char in content:
        if char.isdigit(): number += char
        else: break
    return int(number)

def getcountingchannel(guild_id):
    res = countcoll.find_one({'guild_id': guild_id})
    if res is None:
        return
    else:
        res = res.get('channel_id')
        return res

def getnumber(guild_id):
    res = countcoll.find_one({'guild_id': guild_id})
    if res is None:
        return 0
    else:
        res = res.get('number')
        return int(res)

def getuser(guild_id):
    res = countcoll.find_one({'guild_id': guild_id})
    if res is None:
        return
    else:
        res = res.get('user_id')
        return int(res)

def resetnumber(guild_id):
    countcoll.update_one({'guild_id': guild_id}, {"$set": {'number': 0}})


def updatenumber(number, author_id, guild_id):
    countcoll.update_one({'guild_id': guild_id}, {'$set': {'number': number, 'user_id': author_id}})
    return

def removecountingchannel(guild_id):
    countcoll.delete_one({'guild_id': guild_id})


def setcountingchannel(channel_id, guild_id):
    countcoll.update_one({'guild_id': guild_id}, {'$set': {'channel_id': channel_id}})


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        try:
            guild_id = message.guild.id

            if message.channel.id != getcountingchannel(guild_id):
                return
            elif not message.content[0].isdigit():
                return
            elif message.content == "":
                return

            guilds_number = getnumber(guild_id)

            if message.author.bot:
                await message.channel.send(f'Numbers from bots or bot accounts are not counted. The next number is `{guilds_number+1}`')
            elif message.author.id == getuser(guild_id):
                resetnumber(guild_id)
                await message.add_reaction("❌")
                await message.channel.send(f'{message.author.mention} ruined it! You cannot do two numbers in a row')
            else:
                users_number = clean(message.content)

                if users_number != guilds_number + 1:
                    resetnumber(guild_id)
                    await message.add_reaction("❌")
                    await message.channel.send(f'{message.author.mention} Ruined it!')
                else:
                    updatenumber(users_number, message.author.id, guild_id)
                    await message.add_reaction("✅")
                    if str(users_number).endswith("69"):
                        await message.add_reaction("👌")
                    elif users_number == 100:
                        await message.add_reaction("💯")
                    elif users_number == 1000:
                        await message.add_reaction("😱")
        except:
            pass

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def set(self, ctx):
        res = countcoll.find_one({'guild_id': ctx.guild.id})
        if res is None:
            countcoll.insert_one({'guild_id': ctx.guild.id,
                                  'channel_id': ctx.message.channel.id,
                                  'number': 0,
                                  'user_id': 69420})
        elif res is not None:
            setcountingchannel(ctx.channel.id, ctx.guild.id)
        await ctx.reply("Set the current channel as counting channel")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def remove(self, ctx):
        removecountingchannel(ctx.guild.id)
        await ctx.reply("Removed the counting channel")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if not payload.guild_id:
            return
        if payload.channel_id != getcountingchannel(payload.guild_id):
            return

        message = payload.cached_message
        if not message: return
        if not message.content: return

        if message.content[0].isdigit():
            number = clean(message.content)
            last_number = getnumber(message.guild.id)
            if number == last_number:
                await message.channel.send(f'The last number was deleted. The next number is `{last_number+1}`')


    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):


        if not payload.guild_id:
            return
        if payload.channel_id != getcountingchannel(payload.guild_id):
            return

        message = payload.cached_message
        if not message: return
        if not message.content: return

        if message.content[0].isdigit():
            number = clean(message.content)
            last_number = getnumber(message.guild.id)
            if number == last_number:
                await message.channel.send(f"The last number was edited. The next number is `{last_number+1}`")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if not payload.guild_id:
            return
        if payload.channel_id != getcountingchannel(payload.guild_id):
            return
        if payload.user_id == self.client.user.id:
            return
        if not payload.emoji.is_unicode_emoji():
            return
        if payload.emoji.name not in ["✅", "☑️", "✔️"]:
            return

        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        count = 0
        for reaction in message.reactions:
            if reaction.emoji in ["✅", "☑️", "✔️"]:
                count += reaction.count

        if count == 1:
            last_number = getnumber(payload.guild_id)
            await channel.send(f"A message was given a fake check. The next number is `{last_number+1}`")


def setup(client):
    client.add_cog(Counting(client))
