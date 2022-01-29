from typing import Optional
import discord
from discord import guild
from discord import emoji
from discord.ext import commands
import random
from discord.member import Member
import roasts
from roasts import roastsList
import datetime
import time
import math


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def sus(self, ctx, member: Optional[Member]):

        member = member or ctx.author

        susnum = random.randint(0,101)
        if member is None:
            member = ctx.message.author
        embed = discord.Embed(title = "Sus", description = (f"{member.mention} is {susnum}% Sus"))
        if susnum == 100:
            embed.set_footer(text = 'impostore detected')
        elif susnum > 60:
            embed.set_footer(text = 'sussy baka')
        else:
            embed.set_footer(text = 'not so sus...')       
        await ctx.send(embed=embed)



    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title = 'Invite Ezebot to your server!', description = 'Invite: https://discord.com/api/oauth2/authorize?client_id=804613612857327617&permissions=8&scope=bot%20applications.commands')
        await ctx.send(embed = embed)

    @commands.command() #command to check the bot's latency
    async def ping(self, ctx):
        before = time.monotonic()
        embed = discord.Embed(title = 'Bot Latency', description = f'Pong!\nAPI Latency: {round(self.client.latency * 100)}ms\nMessage Latency: Calculating...')
        message = await ctx.send(embed = embed)
        msgping = (time.monotonic() - before) * 1000
        after_embed = discord.Embed(title = 'Bot Latency', description = f'Pong!\n**API Latency:** {round(self.client.latency * 100)}ms\n**Message Latency:** {int(msgping)}ms')
        await message.edit(embed = after_embed)


    @commands.command()
    async def roast(self, ctx):
        roasts = roastsList
        await ctx.send(random.choice(roasts))


    @commands.command(aliases=['8ball']) #a simple 8ball command
    async def _8ball(self, ctx,*,question):
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.hahahaha",
                    "My sources say no.lol",
                    "Outlook not so good.",
                    "Very doubtful.",
                    "I dont know. Im just a discord bot.",
                    "Ummm no.",
                    "I guess",
                    ]
        embed = discord.Embed(title="8-ball" , description=f'Question: {question}\nAnswer: {random.choice(responses)}' , colour=discord.Colour.dark_magenta())
        await ctx.send(embed=embed)
        
        

    @commands.command() #check how many guilds the bot is in. needs manage messages to work
    @commands.is_owner()
    async def guildcount(self, ctx):
        embed = discord.Embed().add_field(name="Server Count", value=len(self.client.guilds), inline=True)
        await ctx.send(embed=embed)


    @commands.command() #check which guilds the bot is in. needs manage messages to work
    @commands.is_owner()
    async def guilds(self, ctx):
        names = []
        for guild in self.client.guilds:
          names.append(guild.name)
        embed = discord.Embed(title = "Server Names", description="\n".join(names), colour=discord.Colour.green())
        await ctx.send(embed=embed)

    

    @commands.command()
    async def avatar(self, ctx, member : discord.Member):
        useravaurl = member.avatar.url
        await ctx.send(useravaurl)

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @commands.command()
    async def uptime(self, ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title = 'Bot Uptime', description = f'The Uptime is currently {uptime}.')
        embed.set_footer(text = ctx.message.created_at)
        await ctx.send(embed = embed)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        

        embed = discord.Embed(
            title = "Thank you for adding me to your server! 💖",
            description = "Heres some steps you can do to get started:\n\n1. Drag the Bot's role to the top of the heirarchy in the server settings. This willl ensure proper Moderation.\n2. Change the Bot's prefix to the desired one. The default is ``!``, But a lot of bots use the same, and it will conflict. So, do this:\n    >If the other bots have a dashboard, go there and change their prefix temporarily.\n    >Then, change my prefix using the ``!prefix`` command.\n    >Change the other bots' prefixes back to the desired ones.\n3. Use ``!help`` to get familiar with the commands.\n\n And, that's it to get started!\n\n**Note:** The bot is still heavily under development, so please expect a few bugs, and bad uptime(the time the bot is online and can be used). If I am in the server, I will let you know if there are some bugs.",
            color = discord.Colour.green()
        )

        embed.set_footer(text = "Thank You | ")

        await guild.owner.send(embed = embed)
        await guild.owner.send(f'{guild.owner.mention}, These Steps will make sure that all the commands run as desired and will prevent errors.')


    @commands.command()
    async def poll(self, ctx, *, poll_desc):
        embed = discord.Embed(title = "Poll Started", description = poll_desc, color = discord.Colour.blurple())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
        m = await ctx.send(embed = embed)
        await m.add_reaction(emoji = "\N{THUMBS UP SIGN}")
        await m.add_reaction(emoji = "\N{THUMBS DOWN SIGN}")


def setup(client):
    client.add_cog(Misc(client))