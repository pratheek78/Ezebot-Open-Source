
from os import name
from typing import Text
import discord
from discord import embeds
from discord.ext import commands
import asyncio
import random
import aiohttp
from io import BytesIO
from typing import Optional





class Moderation(commands.Cog):




    def __init__(self, client):
        self.client = client

    """THIS SHIT IS COMMENTED OUT CUZ IT IS NOW IN CHANNEL_MODERATION, BUT WE COULD NEED IT SOON SO YEAH"""


    
 #   @commands.command(aliases = ["lock"])
 #   @commands.has_permissions(administrator = True)
  #  async def lockdown(self, ctx, channel : discord.TextChannel = None):
  #      channel = channel or ctx.channel
   #     overwrite = channel.overwrites_for(ctx.guild.default_role)
    #    overwrite.send_messages = False
     #   await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
     #   embed = discord.Embed(title = "Lockdown", description = "🔐This channel is now locked.")
      #  await ctx.send(embed=embed)



 #   @commands.command()
   # @commands.has_permissions(administrator = True)
  #  async def unlock(self, ctx, channel : discord.TextChannel = None):
     #   channel = channel or ctx.channel
     #   overwrite = channel.overwrites_for(ctx.guild.default_role)
       # overwrite.send_messages = True
       # await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
       # embed = discord.Embed(title = "Unlock", description = "🔓This channel is now unlocked for all users" )
      #  await ctx.send(embed=embed)



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
            embed = discord.Embed(title = "Can't Ban User", description = f"You can't Ban {member.mention}, as they have the same perms as you do.")
            await ctx.send(embed = embed)

        else:
            await ctx.guild.kick(user = member, reason = reason)
            embed = discord.Embed(title = "Kick", description = f"{member.mention} Was kicked from the server\nReason: {reason}", colour = discord.Colour.red())
            await ctx.send(embed=embed)
            await member.send(f"You were Kicked from {ctx.guild.name}. Reason: {reason} ")
        


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = "Missing Argument", description = "Please Pass in all required arguments.\n```!kick <user> <reason>```")
            await ctx.send(embed = embed)



    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def dban(self, ctx, member: discord.Member,*,reason = None):

        if member == ctx.guild.owner:
            embed = discord.Embed(title = "Can't Ban Member", description = f'You Cannot Ban {member.mention}, as they are the server owner.')
            await ctx.send(embed = embed)        

        elif member.top_role > ctx.author.top_role:
            embed = discord.Embed(title = "Can't Ban Member", description = f"You do not have permission to ban {member.mention}, as their role is higher than yours.")
            await ctx.send(embed = embed)

        elif member == ctx.author:
            embed = discord.Embed(title = "You Can't Ban Yourself")
            await ctx.send(embed = embed)
            
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title = "Can't Ban Member", description = f"You can't Ban {member.mention} as they have the same permissions as you")
            await ctx.send(embed=embed)


        else:
            await ctx.guild.ban(user = member, reason = reason)
            embed = discord.Embed(title = "Ban", description = f"{member.mention} Was banned from the server\n Reason: {reason}", colour = discord.Colour.red())
            await ctx.send(embed=embed)
            await member.send(f"You were Banned from {ctx.guild.name}. Reason: {reason} ")
    


    @dban.error
    async def dban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = "Missing Argument", description = "Please Pass in all required arguments.\n```!dban <user> <reason>```")
            await ctx.send(embed = embed)




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




    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_guild = True)
    async def unmute(self, ctx, member : discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f" you have unmuted from: - {ctx.guild.name}")
        embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)




    @commands.command(description="Mutes the specified user.", aliases = ["moot"])
    @commands.has_permissions(manage_guild = True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):

        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=True, send_messages=False, read_message_history=True, read_messages=True)
        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" you have been muted from: {guild.name} reason: {reason}")
      



    @commands.command(aliases = ["tm","temp"], description = "Mutes the specified user for a particular amount of time")
    @commands.has_permissions(manage_guild = True)
    async def tempmute(self, ctx, member : discord.Member, time, *, reason = None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        time_convert = {"s":1, "m":60, "h":3600,"d":86400, 'mo':2628288, 'y': 31536000}
        tempmute = int(time[0]) * time_convert[time[-1]]
        await member.add_roles(mutedRole)
        embed = discord.Embed(title = "Muted", description = f'✅ {member.mention} was muted for {time}')
        await ctx.send(embed=embed)
        await asyncio.sleep(tempmute)
        await member.remove_roles(mutedRole)



    @commands.command(aliases = ["slowmode"])
    @commands.has_permissions(manage_guild = True)
    async def slow(self, ctx, seconds: int):
        
        await ctx.channel.edit(slowmode_delay = seconds)

        embed = discord.Embed(title="Slowmode", description=f"The channel slowmode is now set to {seconds}")
        await ctx.send(embed = embed)
    
    
    @commands.command(aliases = ['yeet'])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member,*,reason = None):
        """Bans the specified User"""

        if member == ctx.guild.owner:
            embed = discord.Embed(title = "Can't Ban Member", description = f'You Cannot Ban {member.mention}, as they are the server owner.')
            await ctx.send(embed = embed)

        elif member.top_role > ctx.author.top_role:
            embed = discord.Embed(title = "Can't Ban Member", description = f"You do not have permission to ban {member.mention}, as their role is higher than yours.")
            await ctx.send(embed = embed)

        elif member == ctx.author:
            embed = discord.Embed(title = "You Can't Ban Yourself")
            await ctx.send(embed = embed)
            
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title = "Can't Ban Member", description = f"You can't Ban {member.mention} as they have the same permissions as you")
            await ctx.send(embed=embed)


        else:
            await ctx.guild.ban(user = member, reason = reason, delete_message_days = 0)
            embed = discord.Embed(title = "Ban", description = f"{member.mention} Was banned from the server\n Reason: {reason}", colour = discord.Colour.red())
            await ctx.send(embed=embed)
            await member.send(f"You were Banned from {ctx.guild.name}. Reason: {reason} ")



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
                        embed.set_footer(Text = f'._. | {r.status}')

                        await ctx.send(embed = embed)
                
                except discord.HTTPException:
                    embed = discord.Embed(title = 'File Size too Large', description = f'This File is too large in size. It needs to be under 256kb to get added', colour = discord.Colour.red())
                    await ctx.send(embed = embed)
        






def setup(client):
    client.add_cog(Moderation(client))

    
