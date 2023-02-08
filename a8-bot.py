import os
import random
import uuid

import discord
from discord.ext import commands

import re
 
 
def FindURL(strIn):
 
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, strIn)
    return [x[0] for x in url]
 


token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == my_guild:
            break

    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    

#@bot.command()
#async def astro8(ctx, *args):
#  	response = ""
    
#    # Make sure the user isn't trying to use image only mode, because this is necessary for the bot's functionality
#    if "--imagemode" in args:
#        response = "Unable to process request, you are not allowed to use the `--imagemode` option"
#    else:
#        # Create random ID for this program
#        rand_id = str(uuid.uuid1())
#        print("Process with uuid: \"" + rand_id + "\" started.")
#        # Run the astro8 emulator
#  	    subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8')
#        
#
#    await ctx.channel.send(response)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_content = message.content.lower()
    codeContent = "".join(message_content.split('\n')[1:])
    url = ""
    if len(FindURL(codeContent)) != 0:
        url = FindURL(codeContent)[0]
    if "/astro8" in message_content:
        # Make sure the user isn't trying to use image only mode, because this is necessary for the bot's functionality
        if "--imagemode" in message_content:
            response = "Unable to process request, you are not allowed to use the `--imagemode` option"
        else:
            await bot.send_message(message.channel, "Started `astro8` with arguments: \"" + "".join(message_content.split()[1:]) + "\"\n\n ***Now please provide a file OR url to execute in this instance:***")
            msg = await bot.wait_for_message(timeout= 30, author=message.author, check=check)
            if msg is None:
                await bot.send_message(message.channel, "```diff\n- No input file or URL provided\n```")
                return

            # Create random ID for this program
            rand_id = str(uuid.uuid1())
            print("Process with uuid: \"" + rand_id + "\" started.")
            # Run the astro8 emulator
            programOutput = subprocess.run(['~/Code/Astro8-Computer/Astro8-Emulator/linux-build/astro8', message_content.split()[1:]], stdout=subprocess.PIPE).stdout.decode('utf-8')
        

    await ctx.channel.send(response)

bot.run(token)
