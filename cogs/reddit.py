import discord
from discord.ext import commands
import asyncpraw
import random
import requests
import pymongo
import os

from re import sub
from dotenv import load_dotenv
from discord.ui import View

load_dotenv()
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MONGOCONN = os.getenv('Mongo_conn')
CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')
USERNAME = os.getenv('username')
PASSWORD = os.getenv('red_passwd')
USR_AGENT = os.getenv('agent')

cl = pymongo.MongoClient(MONGOCONN)
db = cl["Ezebot"]


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def meme(self, ctx):

        reddit = asyncpraw.Reddit(client_id = str(CLIENT_ID),
                            client_secret = str(CLIENT_SECRET),
                            username = str(USERNAME),
                            password = str(PASSWORD),
                            user_agent = str(USR_AGENT))


        subreddit = await reddit.subreddit("memes")

        all_subs = []

        hot = subreddit.hot(limit = 50)

        async for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(title = name)
        embed.set_image(url = url)

        refresh = discord.ui.Button(label="Next Meme", style = discord.ButtonStyle.green, emoji="👋")

        async def button_callback(interaction):
            name = random_sub.title
            url = random_sub.url
            new_em = discord.Embed(title = name)
            new_em.set_image(url = url)
            await interaction.edit_message(embed = new_em)

        refresh.callback = button_callback

        view = View()
        view.add_item(refresh)
        await ctx.send(embed=embed, view=view)



    @commands.command(aliases = ['cats', 'kitten'])
    async def cat(self, ctx):
        url = 'https://cataas.com/cat'

        r = requests.get(url)

        embed = discord.Embed(title = "Cat")

        embed.set_image(url = url)

        await ctx.send(embed = embed)




    @commands.command(aliases = ['dogs', 'puppy'])
    async def dog(self, ctx):
        reddit = asyncpraw.Reddit(client_id = "DiQddBWNLE-0cmosbzg4tQ",
                            client_secret = "XR_tFijvMWzvAJyf2f7NbwGWX6QHeA",
                            username = "pratheek78",
                            password = "saravu78",
                            user_agent = "kachua")

        kitty_subs = ['dogs']


        subreddit = await reddit.subreddit(random.choice(kitty_subs))

        all_subs = []

        hot = subreddit.hot(limit = 50)

        async for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(title = name)
        embed.set_image(url = url)

        await ctx.send(embed=embed)

    @commands.command(aliases = ['aww'])
    async def cute(self, ctx):
        reddit = asyncpraw.Reddit(client_id = "DiQddBWNLE-0cmosbzg4tQ",
                            client_secret = "XR_tFijvMWzvAJyf2f7NbwGWX6QHeA",
                            username = "pratheek78",
                            password = "saravu78",
                            user_agent = "kachua")

        kitty_subs = ['aww']


        subreddit = await reddit.subreddit(random.choice(kitty_subs))

        all_subs = []

        hot = subreddit.hot(limit = 50)

        async for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(title = name)
        embed.set_image(url = url)

        await ctx.send(embed=embed)

    


def setup(client):
    client.add_cog(Reddit(client))