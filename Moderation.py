import discord, aiohttp, random, os, pymongo


from discord.ext import commands
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

MONGOCONN = os.getenv('Mongo_conn')
cl = pymongo.MongoClient(MONGOCONN)
mdb = cl['Ezebot']
modcoll = mdb['Modlogging']


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases = ['purge'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def badname(self, ctx, member : discord.Member):
        part1 = ["Hot",
                 "Cold",
                 "Big",
                 "Small",
                 "Sour",
                 "Sweet",
                 "Spicy"]

        part2 = ["Apple",
                 "Orange",
                 "Banana",
                 "Cherry",
                 "Tomato"]

        part3 = ["Cake",
                 "Pancake",
                 "Pie",
                 "Chips",
                 "Cookie"]


        namepart1 = random.choice(part1)
        namepart2 = random.choice(part2)
        namepart3 = random.choice(part3)
        
        await member.edit(nick = f'{namepart1} {namepart2} {namepart3}')


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def goodname(self, ctx, member : discord.Member):
        await member.edit(nick=None)


    @commands.command(aliases = ["slowmode"])
    @commands.has_permissions(manage_guild = True)
    async def slow(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay = seconds)
        embed = discord.Embed(title="Slowmode", description=f'The channel slowmode is now set to {seconds}')
        await ctx.send(embed = embed)



    @commands.command(aliases=["stealemoji", "emoji"])
    @commands.has_permissions(manage_emojis = True)
    async def addemoji(self, ctx, url: str, *, name):
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgOrGif = BytesIO(await r.read())
                    bValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image = bValue, name = name)
                        embed = discord.Embed(title = 'Emoji Added',
                                              description = f'Emoji Succesfully Added with name :{name}:',
                                              colour = discord.Colour.green())
                        await ctx.send(embed = embed)
                        await ses.close()
                
                    else:
                        embed = discord.Embed(title = 'Error While Adding emoji', 
                                              description = 'There was an Error while adding the emoji. Check the perms and then rerun the command.',
                                              colour = discord.Colour.red())
                        embed.set_footer(text = f'._. | {r.status}')

                        await ctx.send(embed = embed)
                
                except discord.HTTPException:
                    embed = discord.Embed(title = 'File Size too Large', description = f'This File is too large in size. It needs to be under 256kb to get added', colour = discord.Colour.red())
                    await ctx.send(embed = embed)
        


def setup(client):
    client.add_cog(Moderation(client))

    
