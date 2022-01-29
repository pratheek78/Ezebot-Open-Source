import discord
from discord.ext import commands
import googletrans

class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['trans'])
    async def translate(self, ctx, lang_to, *args):
        lang_to = lang_to.lower()
        if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
            await ctx.send('Not A Valid Language')
        
        text = ' '.join(args)
        translator = googletrans.Translator()
        text_translated = translator.translate(text, dest=lang_to).text
        await ctx.send(text_translated)






def setup(client):
    client.add_cog(Translate(client))

