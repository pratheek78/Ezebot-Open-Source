import discord
from discord.ext import commands

class slashcmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def hello(self, ctx):
        await ctx.respond(f'Hello, {ctx.author}')


def setup(client):
    client.add_cog(slashcmds(client))