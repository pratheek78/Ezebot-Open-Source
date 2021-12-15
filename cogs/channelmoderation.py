
from discord.ext import commands
from discord import Embed, Member, User, channel, utils
import asyncio, discord
from typing import Dict, List, Pattern, Set, Tuple, Union

from googlesearch import search

red = 0xff0000
green = 0x34eb40


class channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="google", aliases=["g"])
    async def google(self, ctx, *, text):
        if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
            searchContent = f"{text}"
            searchContent = searchContent + text

            for j in search(f"{text}", tld="co.in", num=1, stop=1, pause=2):
                
                await ctx.channel.send(f"{j}")
                
   
    
    @commands.command(name="show", aliases=["s"])
    async def _show(self, ctx, member: Member):
        if ctx.author.guild_permissions.manage_messages:
           channel = ctx.channel
           guild = ctx.message.guild
           await channel.set_permissions(target=member, view_channel = True)
           embed = Embed(title='Success!', description=f"Revealed {channel.mention} to {member.mention}. ", colour=red)
           await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)
    
    
    @commands.command(name="hide", aliases=["h", "noq"])
    async def _hide(self, ctx, member: Member):
        if ctx.author.guild_permissions.manage_messages:
           channel = ctx.channel
           guild = ctx.message.guild
           await channel.set_permissions(target=member, view_channel = False)
           embed = Embed(title='Success!', description=f"Hid {channel.mention} from {member.mention}. ", colour=red)
           await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="createchannel", aliases=["createch"])
    @commands.has_permissions(manage_channels = True)
    async def _CreateChannel(self, ctx, *, name=None):
        guild = ctx.message.guild

        cat = ctx.channel.category     
        discord.utils.get(ctx.guild.categories, id=cat)

        await guild.create_text_channel(name=name, category=cat)
        embed = discord.Embed(title=f"Channel {name} has been created!", colour=red)
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command(name="deletechannel", aliases=["deletech"])
    async def _DeleteChannel(self, ctx, textchannel: discord.TextChannel):
        guild = ctx.message.guild
        if ctx.author.guild_permissions.administrator:
            await textchannel.delete()
            embed = discord.Embed(title=f"Channel {textchannel} has been deleted!", colour=red)
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)

    
    @commands.command(name="lockdown", aliases=["ld"])       ## Needs fixing!
    async def _Lockdown(self, ctx):
        channel = ctx.channel
        default_role = ctx.guild.default_role
        if ctx.author.guild_permissions.administrator:
            await channel.set_permissions(target=default_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
            embed = discord.Embed(title=f"Sucessfully locked down {channel}!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)





def setup(bot):
    bot.add_cog(channel(bot))
            
