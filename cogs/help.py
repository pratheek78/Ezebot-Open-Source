import discord
from discord import message
from discord import embeds
from discord.ext import commands
from discord.ui.select import select
from typing import Optional











class HelpView(discord.ui.View):
    @discord.ui.select(placeholder='Select A Command Category Here', options=[
        discord.SelectOption(label='Moderation', description="Shows Info About All the moderation commands.",
                             emoji='🔨', value='moderation'),
        discord.SelectOption(label='Administration', description="Shows info about all the admin commands", emoji='⚙️',
                             value='admin'),
        discord.SelectOption(label='Information', description="Shows All the Info Commands", emoji='❓', value='info'),
        discord.SelectOption(label='Fun', description="Shows All the Fun Commands", emoji='🎠', value='fun'),
        discord.SelectOption(label="Misc", description="Shows the Misc Commands", emoji='🎭', value='misc')
    ])
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        if select.values[0] == 'moderation':
            moderation_embed = discord.Embed(title = 'Moderation', colour = discord.Colour.red())
            fields = [("``Kick``", 'Kicks the Specified Member', True),
                      ("``Ban``", "Bans the Specified Member", True),
                      ("``dban``", "Bans the Member and also deletes their past 24 hours of messages(to be fixed soon)", True),
                      ("``Clear``", "Clears the specified amount of messages from the channel", False),
                      ("``badname``", "Replaces the member's nickname with a random(sometimes funny) one.", True),
                      ("``goodname``", "Resets the member's nickname", True),
                      ("``Mute``", "Mutes the member. You might have to change channel permissions of a few staff roles for it to have an effect on them as well", False),
                      ("``Unmute``", "Unmutes the member", True),
                      ("``Tempmute``", "Mutes the member and unmutes them automatically after the specified time.", True),
                      ("``Slowmode``", "Sets the channel slowmode", False)]
            for name, value, inline in fields:
                moderation_embed.add_field(name = name, value = value, inline =  inline)

            await interaction.message.edit(embed=moderation_embed)  
                    

        
        elif select.values[0] == 'admin':
            admin_embed = discord.Embed(title = 'Administration', colour = discord.Colour.orange())

            fields = [("``addemoji``", "Adds an emoji", True),
                      ("``prefix``", "Changes the bot's prefix to the one specified", True),
                      ("``automod``", "Turns the automod on or off. The moderation is done using an AI. This feature is under developement so please refrain from using it.", True),
                      ("``show``", "Reveals the channel to a particular member", True),
                      ("``hide``", "Hides the channel to a particular member", True),
                      ("``createchannel``", "Creates a channel with the specified name", True),
                      ("``deletechannel``", "Deletes the specified channel", True),
                      ("``lockdown``", "Locks down the channel (needs fixing so as to work with verification systems in servers)", True)]
        
            for name, value, inline in fields:
                admin_embed.add_field(name = name, value = value, inline =  inline)

            await interaction.message.edit(embed=admin_embed)



        elif select.values[0] == 'info':
            info_embed = discord.Embed(title = 'Information', colour = discord.Colour.green())

            fields = [("``serverinfo``", "Retrieves Info about the server", True),
                      ("``userinfo``", "Retrieves info about a user. Currently under development", True),
                      ("``wiki``", "Retrieves a summary of the wikipedia article of the term specified. The term will have to be very specific.", True)]

            for name, value, inline in fields:
                info_embed.add_field(name = name, value = value, inline =  inline)

            await interaction.message.edit(embed=info_embed)


        elif select.values[0] == 'fun':
            fun_embed = discord.Embed(title = 'Fun', colour = discord.Colour.yellow())

            fields = [("``sus``", "Checks if the user is a sussy baka", True),
                      ("``roast``", "Sends a random roast", True),
                      ("``8ball``", "Sends a random response to a question", True),
                      ("``avatar``", "Shows the user's avatar", True),
                      ("``meme``", "Sends a random meme from the r/memes subreddit", True),
                      ("``cat``", "Sends a random post from the r/cats subreddit", True),
                      ("``dog``", "Sends a random post from the r/dogs subreddit", True),
                      ("``cute``", "Sends a random post from the r/aww subreddit", True)]

            for name, value, inline in fields:
                fun_embed.add_field(name = name, value = value, inline =  inline)

            await interaction.message.edit(embed=fun_embed)

        elif select.values[0] == 'misc':
            misc_embed = discord.Embed(title = 'Misc', colour = discord.Colour.blurple())

            fields = [("``uptime``", "Shows how long the bot has been running for", True),
                      ("``invite``", "Invite the Bot to your server!", True),
                      ("``ping``", "Shows the API and Message latency", True),
                      ("``translate``", "Translates the specified text from one language to the specified one", True),
                      ("``calc``", "Calculates the specified problem. Note: Does not solve equations.", True)]


            for name, value, inline in fields:
                misc_embed.add_field(name = name, value = value, inline =  inline)

            await interaction.message.edit(embed=misc_embed)




class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def help(self, ctx, cmd: Optional[str]):
        if cmd is not None:

            cmd = cmd.lower()


            if cmd == "kick":
                embed = discord.Embed(title = "Kick", description = "Kicks the Specified user\n\n**Permissions Required:**\nKick Members\n\n**Usage:**\n```!kick <user> <reason>```")
                await ctx.send(embed=embed)

            elif cmd == "ban":
                embed = discord.Embed(title = "Ban", description = "Bans the specified user\n\n**Permissions Required:**\nBan Members\n**Aliases:**\n!yeet\n\n**Usage:**\n```!ban <user> <reason>```")
                await ctx.send(embed = embed)

            elif cmd == "clear":
                embed = discord.Embed(title = "clear", description = "Clears the specified amount of messages in the channel\n\n**Permissions Required:**\nManage Messages\n**Aliases**\n!purge\n\n**Usage:**\n```!clear <amount>```")
                await ctx.send(embed = embed)

            elif cmd == "badname":
                embed = discord.Embed(title = "badname", description = "Replaces the member's name with a Random nickname(Sometimes Funny, and also cringe)\n\n**Permissions Required:**\nManage Nicknames\n```!badname <user>```")
                await ctx.send(embed = embed)

            elif cmd == "goodname":
                embed = discord.Embed(title = "goodname", description = "Resets the member's nickname\n\n**Permissions Required:**\nManage Nicknames\n**Usage:**\n```!goodname <user>```")
                await ctx.send(embed = embed)

            elif cmd == "mute":
                embed = discord.Embed(title = "mute", description = "Mutes the specified member until the ``!unmute`` command is run\n\n**Permissions Required:**\nManage Server\n\n**Usage:**\n```!mute <user>```")
                await ctx.send(embed = embed)  

            elif cmd == "tempmute":
                embed = discord.Embed(title = "tempmute", description = "Mutes the member for the specified amount of time\n\n**Permissions Required:**\nManage Server\n**Aliases:**\n``!tm``\n\n**Usage:**\n```!tempmute <user> <time>```")
                await ctx.send(embed = embed)

            elif cmd == "unmute":
                embed = discord.Embed(title = "unmute", description = "Unmutes the specified member\n\n**Permissions Required:**\nManage Server\n\n**Usage:**\n```!unmute <member>")
                await ctx.send(embed = embed)

            elif cmd == "slowmode":
                embed = discord.Embed(title = "slowmode", description = "Sets the channel slowmode\n\n**Permissions Required:**\nManage Server\n\n**Usage:**\n```!slowmode <time>```")
                await ctx.send(embed = embed)

            elif cmd == "addemoji":
                embed = discord.Embed(title = "addemoji", description = "Adds the emoji to the server using the link. The file needs to be under 256kb\n\n**Permissions Required:**\nManage Emojis\n\n**Usage:**\n```!addemoji <url> <name>```")
                await ctx.send(embed = embed)  

            elif cmd == "prefix":
                embed = discord.Embed(title = "prefix", description = "Changes the Bot's prefix in the server(You may have to change other bots' prefix temporarily for this to not conflict. It depends on what prefix they have)\n\n**Permissions Required:**\nAdministrator\n\n**Usage:**\n```!prefix <newprefix>```")
                await ctx.send(embed = embed)

            elif cmd == "automod":
                embed = discord.Embed(title = "Command under development")    
                await ctx.send(embed = embed, delete_after = 5)

            elif cmd == "show":
                embed = discord.Embed(title = "show", description = "Shows a channel to a specific user\n\n**Permissions Required:**\nManage Messages\n\n**Usage:**\n```!show <user>```")
                embed.set_footer(text = "You MUST use this in the channel you want to show, not in any other channel")
                await ctx.send(embed = embed)

            elif cmd == "hide":
                embed = discord.Embed(title = "Hide", description = "Hides a channel from a specific user\n\n**Permissions Required:**\nManage messages\n\n**Aliases:**\n``!noq``\n\n**Usage:**\n```!hide <user>```")
                embed.set_footer(text = "You MUST use this in the channel you want to hide, not in any other channel")
                await ctx.send(embed = embed)

            elif cmd == "createchannel":
                embed = discord.Embed(title = "createchannel", description = "Creates a channel with the specified name\n\n**Permissions Required:**\nManage Channels\n\n**Usage:**\n```!createchannel <channel name>```")
                await ctx.send(embed = embed)

            elif cmd == "deletechannel":
                embed = discord.Embed(title = "deletechannel", description = "Deletes the specified channel\n\n**Permissions Required:**\nManage Channels\n\n**Usage:**\n```!deletechannel <channel>```")
                await ctx.send(embed = embed)

            elif cmd == "lockdown":
                embed = discord.Embed(title = "lockdown", description = "Locks down the channel(NOTE: This could potentially mess up your verification system. A fix is being worked on. If you dont have one, you have nothing to worry about)\n\n**Permissions Required:**\nManage Server\n\n**Usage:**\n```!lockdown```")
                await ctx.send(embed = embed)

            elif cmd == "serverinfo":
                embed = discord.Embed(title = "serverinfo", description = "Lists all info about the server\n\n**Aliases**\n``!si``, ``!gi``**Usage:**\n```!si```")
                await ctx.send(embed = embed) 

            elif cmd == "userinfo":
                embed = discord.Embed(title = "userinfo", description = "Lists all available info about the user. Currently working on adding more info\n\n**Aliases:**\n``!ui``, ``!whois``\n\n**Usage:**\n```!ui <user>[Optional]```")  
                await ctx.send(embed = embed)

            elif cmd == "wiki":
                embed = discord.Embed(title = "wiki", description = "Retrieves wiki information about the specified topic. NOTE: Be very specific with the topic you type.\n\n**Usage:**\n```!wiki <topic>```")
                await ctx.send(embed = embed) 

            elif cmd == "sus":
                embed = discord.Embed(title = "sus", description = "Checks if the user is a sussy baka(sorry, I had to)\n\n**Usage:**\n```!sus <user>[Optional]```")
                await ctx.send(embed = embed)

            elif cmd == "roast":
                embed = discord.Embed(title = "roast", description = "Sends a random roast\n\n**Usage:**\n```!roast```")
                await ctx.send(embed = embed)

            elif cmd == "8ball":
                embed = discord.Embed(title = "8ball", description = "A simple 8ball command\n\n**Usage:**\n```!8ball <question>```")
                await ctx.send(embed = embed)

            elif cmd == "avatar":
                embed = discord.Embed(title = "avatar", description = "Sends the specified user's Profile picture\n\n**Usage:**\n```!avatar <user>[Optional]```")
                await ctx.send(embed = embed)   

            elif cmd == "meme":
                embed = discord.Embed(title = "meme", description = "Sends a random meme fro the r/memes subreddit\n\n**Usage:**\n```!meme```")
                await ctx.send(embed = embed)

            elif cmd == "cat":
                embed = discord.Embed(title = "cat", description = "Sends a random cat image\n\n**Usage:**\n```!cat```")
                await ctx.send(embed = embed)

            elif cmd == "dog":
                embed = discord.Embed(title = "dog", description = "Sends a random dog image\n\n**Usage:**\n```!dog```")
                await ctx.send(embed = embed)

            elif cmd == "uptime":
                embed = discord.Embed(title = "uptime", description = "Check how long the bot has been online for\n\n**Usage:**\n```!uptime```")
                await ctx.send(embed = embed)

            elif cmd == "invite":
                embed = discord.Embed(title = "invite", description = "Invite the bot to your server!\n\n**Usage:**\n```!invite```")
                button = discord.ui.Button(label = "Invite Me!", url = "https://discord.com/api/oauth2/authorize?client_id=804613612857327617&permissions=8&scope=bot%20applications.commands")
                view = discord.ui.View()
                view.add_item(button)
                await ctx.send(embed = embed, view = view)

        


        else:
            embed = discord.Embed(title = 'Help', description = 'React to the dropdown below to get help about all the different categories')
            embed.set_thumbnail(url = self.client.user.avatar.url)
            await ctx.send(embed = embed, view = HelpView(timeout=20))
        



def setup(client):
    client.add_cog(HelpCommand(client))