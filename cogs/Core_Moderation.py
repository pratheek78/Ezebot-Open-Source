import discord, pymongo, os, datetime

from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

MONGOCONN = os.getenv('Mongo_conn')
cl = pymongo.MongoClient(MONGOCONN)
mdb = cl['Ezebot']
modcoll = mdb['Modlogging']


class Coremod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member,*,reason = None):
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title = "Can't Kick member", description = f"You Do not have permissions to kick {member.mention}, as their role is higher than yours.")
            await ctx.send(embed = embed)
        elif member == ctx.author:
            embed = discord.Embed(title = "You can't kick yourself")
            await ctx.send(embed = embed)
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title = "Can't Kick User", description = f"You can't Kick {member.mention}, as they have the same perms as you do.")
            await ctx.send(embed = embed)
        else:
            lastcase = modcoll.find_one({'guild_id': ctx.message.guild.id})
            if lastcase is None:
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'kick',
                        'Case Number': 1,
                        'Reason': reason}
                modcoll.insert_one(post)
            elif lastcase is not None:
                lastcase_number = int(lastcase.get('Case Number'))
                newcase_number = lastcase + 1
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'kick',
                        'Case Number': newcase_number,
                        'Reason': reason}
                modcoll.insert_one(post)

                await ctx.guild.kick(user = member, reason = reason)
                embed = discord.Embed(title = "Kick", description = f"{member.mention} Was kicked from the server\nReason: {reason}", colour = discord.Colour.red())
                await ctx.send(embed=embed)
                await member.send(f"You were Kicked from {ctx.guild.name}.\nReason: {reason}\nResponsible Moderator: {ctx.author.name}")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title = "Can't Ban member", description = f"You Do not have permissions to ban {member.mention}, as their role is higher than yours.")
            await ctx.send(embed = embed)
        elif member == ctx.author:
            embed = discord.Embed(title = "You can't Ban yourself")
            await ctx.send(embed = embed)
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title = "Can't Ban User", description = f"You can't Ban {member.mention}, as they have the same perms as you do.")
            await ctx.send(embed = embed)
        else:
            lastcase = modcoll.find_one({'guild_id': ctx.message.guild.id})
            if lastcase is None:
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'ban',
                        'Case Number': 1,
                        'Reason': reason}
                modcoll.insert_one(post)
            elif lastcase is not None:
                lastcase_number = int(lastcase.get('Case Number'))
                newcase_number = lastcase + 1
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'ban',
                        'Case Number': newcase_number,
                        'Reason': reason}
                modcoll.insert_one(post)

            await ctx.guild.ban(user = member, reason = reason, delete_message_days = 0)
            embed = discord.Embed(title = "Ban", description = f"{member.mention} Was banned from the server\nReason: {reason}", colour = discord.Colour.red())
            await ctx.send(embed=embed)
            await member.send(f"You were banned from {ctx.guild.name}.\nReason: {reason}\nResponsible Moderator: {ctx.author.name}")

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def mute(self, ctx, member: discord.Member, time: Optional[str], reason = None):
        guild = ctx.guild
        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400, 'mo': 2628288, 'y': 31536000}
        mutetime = int(time[0]) * time_convert[time[-1]]
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title = "Can't Mute member", description = f"You Do not have permissions to mute {member.mention}, as their role is higher than yours.")
            await ctx.send(embed = embed)
        elif member == ctx.author:
            embed = discord.Embed(title = "You can't Mute yourself")
            await ctx.send(embed = embed)
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title = "Can't Mute User", description = f"You can't Mute {member.mention}, as they have the same perms as you do.")
            await ctx.send(embed = embed)
        else:
            if time is None:
                embed = discord.Embed(title = "Please state the time")
                await ctx.send(embed = embed)
            else:
                await member.timeout(until = discord.utils.utcnow() + datetime.timedelta(seconds = mutetime), reason = reason)
                embed = discord.Embed(title = 'Mute', description = 'Muting member...')
                m = await ctx.send(embed = embed)
                lastcase = modcoll.find_one({'guild_id': ctx.message.guild.id})
                if lastcase is None:
                    post = {'guild_id': ctx.message.guild.id,
                            'member_id': member.id,
                            'moderator': ctx.author.id,
                            'Operation': 'mute',
                            'Case Number': 1,
                            'Reason': reason}
                    modcoll.insert_one(post)
                elif lastcase is not None:
                    lastcase_number = int(lastcase.get('Case Number'))
                    newcase_number = lastcase + 1
                    post = {'guild_id': ctx.message.guild.id,
                            'member_id': member.id,
                            'moderator': ctx.author.id,
                            'Operation': 'mute',
                            'Case Number': newcase_number,
                            'Reason': reason}
                    modcoll.insert_one(post)
                new_em = discord.Embed(title = 'Muted Member', description = f'{member.mention} has been muted for {time}\n**Reason:** {reason}')
                await m.edit(embed = embed)
                dm_embed = discord.Embed(title = 'Mute', description = f'You have been muted in {ctx.guild} for {time}\n**Reason:** {reason}')
                await member.send(embed = dm_embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(until = None)
        embed = discord.Embed(title = 'Unmute', description = f'{member.mention} has been unmuted')
        await ctx.send(embed = embed)
        dm_em = discord.Embed(title = 'Unmute', description = f'You have been unmuted in {ctx.guild}')
        await member.send(embed = dm_em)


def setup(client):
    client.add_cog(Coremod(client))