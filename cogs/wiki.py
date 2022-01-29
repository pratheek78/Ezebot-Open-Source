import discord
from discord.ext import commands
import wikipedia

class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wiki(self, ctx, *, term):
        suggestion = term
        summary = wikipedia.summary(suggestion, sentences = 15)
        page = wikipedia.page(suggestion)

        embed = discord.Embed(
            title=page.title,
            description= summary,
            color=discord.Colour.brand_green()
        )
        embed.set_footer(text = f'Wikipedia | URL: {page.url}')
        embed.set_thumbnail(url = page.images[1])

        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Wiki(client))
