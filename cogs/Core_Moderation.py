import discord, pymongo, os, datetime

from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

MONGOCONN = os.getenv('Mongo_conn')
cl = pymongo.MongoClient(MONGOCONN)
mdb = cl['Ezebot']
modcoll = mdb['Modlogging']
cur_date = str(datetime.date.today()) #Accessed in a lot of commands, so easier to put here instead of declaring every time

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
                newcase_number = 1
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'kick',
                        'Case Number': newcase_number,
                        'Reason': reason,
                        'Date': cur_date}
                modcoll.insert_one(post)

                await ctx.guild.kick(user = member, reason = reason)
                embed = discord.Embed(title = "Kick", description = f"{member.mention} Was kicked from the server\nReason: {reason}", colour = discord.Colour.red())
                embed.set_footer(text = f'Case Number {newcase_number}')
                await ctx.send(embed=embed)
                await member.send(f"You were Kicked from {ctx.guild.name}.\nReason: {reason}\nResponsible Moderator: {ctx.author.name}")
            elif lastcase is not None:   
                list(modcoll.find({'guild_id': ctx.message.guild.id}).sort("Case Number", pymongo.DESCENDING).limit(1))
                             
                last_num = str([ sub['Case Number'] for sub in lastcase ])
                last_num = last_num.lstrip("[").rstrip("]")
                last_num = int(last_num)
                newcase_number = last_num + 1
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'kick',
                        'Case Number': newcase_number,
                        'Reason': reason,
                        'Date': cur_date}
                modcoll.insert_one(post)

                await ctx.guild.kick(user = member, reason = reason)
                embed = discord.Embed(title = "Kick", description = f"{member.mention} Was kicked from the server\nReason: {reason}", colour = discord.Colour.red())
                embed.set_footer(text = f'Case Number {newcase_number}')
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
                newcase_number = 1
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'ban',
                        'Case Number': newcase_number,
                        'Reason': reason,
                        'Date': cur_date}
                modcoll.insert_one(post)

                await ctx.guild.ban(user = member, reason = reason, delete_message_days = 0)
                embed = discord.Embed(title = "Ban", description = f"{member.mention} Was banned from the server\nReason: {reason}", colour = discord.Colour.red())
                embed.set_footer(text=f'Case Number {newcase_number}')
                await ctx.send(embed=embed)
                await member.send(f"You were banned from {ctx.guild.name}.\nReason: {reason}\nResponsible Moderator: {ctx.author.name}")

            elif lastcase is not None:
                lastcase = list(modcoll.find({'guild_id': ctx.message.guild.id}).sort("Case Number", pymongo.DESCENDING).limit(1))
                
                last_num = str([ sub['Case Number'] for sub in lastcase ])
                last_num = last_num.lstrip("[").rstrip("]")
                last_num = int(last_num)
                newcase_number = last_num + 1
                post = {'guild_id': ctx.message.guild.id,
                        'member_id': member.id,
                        'moderator': ctx.author.id,
                        'Operation': 'ban',
                        'Case Number': newcase_number,
                        'Reason': reason,
                        'Date': cur_date}
                modcoll.insert_one(post)

                await ctx.guild.ban(user = member, reason = reason, delete_message_days = 0)
                embed = discord.Embed(title = "Ban", description = f"{member.mention} Was banned from the server\nReason: {reason}", colour = discord.Colour.red())
                embed.set_footer(text=f'Case Number {newcase_number}')
                await ctx.send(embed=embed)
                await member.send(f"You were banned from {ctx.guild.name}.\nReason: {reason}\nResponsible Moderator: {ctx.author.name}")

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def mute(self, ctx, member: discord.Member, time: Optional[str], *, reason = None):
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
                await ctx.send(embed = embed, delete_after = 5)
            else:
                await member.timeout(until = discord.utils.utcnow() + datetime.timedelta(seconds = mutetime), reason = reason)
                embed = discord.Embed(title = 'Mute', description = 'Muting member...')
                m = await ctx.send(embed = embed)
                lastcase = modcoll.find_one({'guild_id': ctx.message.guild.id})
                
                if lastcase is None:
                    newcase_number = 1
                    post = {'guild_id': ctx.message.guild.id,
                            'member_id': member.id,
                            'moderator': ctx.author.id,
                            'Operation': 'mute',
                            'Case Number': newcase_number,
                            'Reason': reason,
                            'Date': cur_date}
                    modcoll.insert_one(post)

                    new_em = discord.Embed(title = 'Muted Member', description = f'{member.mention} has been muted for {time}\n**Reason:** {reason}')
                    new_em.set_footer(text=f'Case Number {newcase_number}')
                    await m.edit(embed = new_em)
                    dm_embed = discord.Embed(title = 'Mute', description = f'You have been muted in {ctx.guild} for {time}\n**Reason:** {reason}')
                    await member.send(embed = dm_embed)

                elif lastcase is not None:
                    lastcase = list(modcoll.find({'guild_id': ctx.message.guild.id}).sort("Case Number", pymongo.DESCENDING).limit(1))
                    
                    last_num = str([ sub['Case Number'] for sub in lastcase ])
                    last_num = last_num.lstrip("[").rstrip("]")
                    last_num = int(last_num)
                    newcase_number = last_num + 1
                    post = {'guild_id': ctx.message.guild.id,
                            'member_id': member.id,
                            'moderator': ctx.author.id,
                            'Operation': 'mute',
                            'Case Number': newcase_number,
                            'Reason': reason,
                            'Date': cur_date}
                    modcoll.insert_one(post)

                    new_em = discord.Embed(title = 'Muted Member', description = f'{member.mention} has been muted for {time}\n**Reason:** {reason}')
                    new_em.set_footer(text=f'Case Number {newcase_number}')
                    await m.edit(embed = new_em)
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

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def delcase(self, ctx, case: int):
        lastcase = modcoll.find_one({'guild_id': ctx.guild.id, 'Case Number': case})
        if lastcase is None:
            await ctx.send('This case does not exist')
        else:
            modcoll.delete_one(lastcase)
            await ctx.send('Case Deleted')

    @commands.command()
    async def case(self, ctx, case: int):
        req_case = modcoll.find_one({'guild_id': ctx.guild.id, 'Case Number': case})
        if req_case is None:
            await ctx.send('This case does not exist')
        else:
            vic_id = req_case.get('member_id')
            mod_id = req_case.get('moderator')
            op = req_case.get('Operation')
            reason = req_case.get('Reason')
            date = req_case.get('Date')
            
            vic = self.client.get_user(vic_id)
            mod = self.client.get_user(mod_id)
            
            embed = discord.Embed(title = f'Case Number {case}',
                                  description = f'**Member:** {vic}\n**Responsible Moderator:** {mod}\n**Operation:** {op}\n**Reason:** {reason}\n**Case:** {case}\n**Date:** {cur_date}',
                                  colour = discord.Colour.blurple())
            await ctx.send(embed = embed)





def setup(client):
    client.add_cog(Coremod(client))