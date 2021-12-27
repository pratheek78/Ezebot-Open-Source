import discord, os, pymongo


from discord.ext import commands
from os import listdir, path
from dotenv import load_dotenv

load_dotenv()
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.getenv('TOKEN')
MONGOCONN = os.getenv('Mongo_conn')


cl = pymongo.MongoClient(MONGOCONN)
mdb = cl["Ezebot"]


def get_prefix(client, message):
    pcol = mdb["prefix"]

    prefix = pcol.find_one({"guild_id": message.guild.id})

    if prefix is not None:
        prefix = prefix.get("prefix")

    else:
        prefix = "!"
        result = pcol.find_one({"guild_id": message.guild.id})
        if result is not None:
            result = result.get("prefix")
        post = {"guild_id": message.guild.id,
                "prefix": prefix}
        pcol.insert_one(post)

    if prefix is None:
        prefix = "!"
        result = pcol.find_one({"guild_id": message.guild.id})
        if result is not None:
            result = result.get("prefix")
        post = {"guild_id": message.guild.id,
                "prefix": prefix}
        pcol.insert_one(post)

    return prefix


owners = [577751099554136064]
client = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all(), owner_ids = owners, case_insensitive = True)
client.remove_command('help')

for cog in listdir(path.join(path.dirname(path.abspath(__file__)), "cogs")):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")

    else:
        print(f'unable to load {cog[:-3]}') #loads in all the cogs in the specified folder


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name = "For Free!")) #sets the bot's presence to watching
    print('Bot is ready!') 
    

@client.event
async def on_message(message):

    pcol = mdb["prefix"]


    if client.user.mentioned_in(message) and message.mention_everyone is False:
        result = pcol.find_one({"guild_id": message.guild.id})
        result = result.get("prefix")

        await message.channel.send(f"My prefix is ``{result[0]}``")
    elif client.user.mentioned_in(message) and message.mention_everyone is False:
        await message.channel.send(f"My prefix is ``!``")


    await client.process_commands(message)


@client.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx, prefix):
    pcol = mdb["prefix"]
    result = pcol.find_one({"guild_id": ctx.guild.id})

    if result is None:
        post = {"guild_id": ctx.guild.id,
                "prefix": prefix}
        pcol.insert_one(post)
        await ctx.send(f'Prefix has been set to ``{prefix}``')
    elif result is not None:
        result = result.get("prefix")
        pcol.update_one({"guild_id": ctx.guild.id}, {"$set":{"prefix": prefix}})
        await ctx.send(f"Prefix has been set to ``{prefix}``")
    else:
        result = "!"


client.run(TOKEN)