import discord, os, pymongo

from discord.ext import commands
from typing import Optional


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

cl = pymongo.MongoClient("")
mdb = cl["Ezebot"]
mcol = mdb["ui_messages"]#outside the class since one event and one command use this same variable



class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return


        else:
            result = mcol.find_one({"guild_id": message.guild.id,
                                    "author_id": message.author.id})



            if result is None:
                post = {"author_id": message.author.id,
                        "messages": 1,
                        "guild_id": message.guild.id}
                mcol.insert_one(post)

            if result is not None:
                mcol.update_one({"guild_id": message.guild.id, "author_id": message.author.id}, {"$inc": {"messages": 1}})


    
    @commands.command(aliases = ['ui', 'whois'])
    async def userinfo(self, ctx, member: Optional[discord.Member]):

        member = member or ctx.author


        if member.bot == True:
            await ctx.send('Cannot Retrieve Info about a Bot.')

        else:
            mes = mcol.find_one({"guild_id": ctx.message.guild.id, "author_id": ctx.message.author.id})
            if mes is not None:
                mes = mes.get("messages")


            embed = discord.Embed(title = "User Info",  
                                colour = discord.Colour.blurple(),
                                timestamp = ctx.message.created_at
                                )

    
            embed.set_thumbnail(url = member.avatar.url)


            fields = [  ("Name", str(member), True),
                        ("Top Role", member.top_role.mention, True),
                        ("Status", str(member.status).title(), False),
                        ("Activity", f"{str(member.activity.type).split('.')[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''} ", True),
                        ("Created On", member.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                        ("Joined On", member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                        ("Booster", bool(member.premium_since), True),
                        ("Total Messages(Counted By Bot)", f'``{mes}``', True),
                        ("Roles", f'{len(member.roles)-1}', False)

                        ]


            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline =  inline)          

            embed.set_author(name = f'{ctx.author.name}')
            embed.set_thumbnail(url = member.avatar.url)

            embed.set_footer(text = f"User ID: {member.id}")
            await ctx.send(embed=embed)



    @commands.command(aliases = ["si", "guildinfo", "gi"])
    async def serverinfo(self, ctx):
        embed = discord.Embed(title = "Server Information",
                              colour = discord.Colour.gold(),
                              timestamp = ctx.message.created_at)
       

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [
                  ("Owner", f'👑{ctx.guild.owner.mention} ({ctx.guild.owner.id})', True),
                  ("Created at", f'{ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S")} GMT', False),
                  ("Region", str(ctx.guild.region).title(), False),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", f'{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}', True),
                  ("Bots", f'{len(list(filter(lambda m: m.bot, ctx.guild.members)))}', True),
                  ("Banned Members", f'{len(await ctx.guild.bans())}', True),
                  ("Statuses", f'🟢{statuses[0]} 🟡{statuses[1]} 🔴{statuses[2]} ⚪{statuses[3]}', False),
                  ("Text Channels", len(ctx.guild.text_channels), False),
                  ("Voice Channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Boosters", f' <a:nitor:905799243992825867> {ctx.guild.premium_subscription_count}', False), #The :nitor: thing is an emoji from a private server
                  ("Verification Level", str(ctx.guild.verification_level).title(), False),
                  ("2FA Moderation", bool(ctx.guild.mfa_level), True),
                  ("Roles", len(ctx.guild.roles), False),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("Features", str(ctx.guild.features), False),
                  ("\u200b", "\u200b", True)
                  ]


        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline =  inline)  

        embed.set_footer(text = f'Server ID: {ctx.guild.id}')
        guild_icon = ctx.message.guild.icon.url
        embed.set_thumbnail(url = guild_icon)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(info(client))
