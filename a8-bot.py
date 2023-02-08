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

import requests
def IsProperURL(url):  # checks status for url, returns false if error or 404
    
    try:
        r = requests.get(url)
        print(url + "\tStatus: " + str(r.status_code))
        if r.status_code == 404:
            return False;
        return True
    except Exception as e:
        print(url + "\tNA FAILED TO CONNECT\t" + str(e))
    return False
 


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

    message_content = message.content
    
    if "/astro8" in message_content.lower():
        # Create random ID for this program
        rand_id = str(uuid.uuid1())
        print("Process with uuid: \"" + rand_id + "\" started.")
        
        codeContent = "".join(message_content.split('\n')[1:])
        url = ""
        if len(FindURL(codeContent)) != 0: # The user is trying to include a file from the web, make sure it is valid.
            url = FindURL(codeContent)[0]
            
            # If the file is pointing to a github address, but isn't the RAW version, change it to the RAW version.
            if "github.com" in url:
                url = url.replace("github.com", "raw.githubusercontent.com")
            
            import urllib.request
            # Check if the file actually exists, and doesn't have a 404 error
            if IsProperURL(url)
                try:
                    # Make url request
                    codeContent = urllib.request.urlretrieve(url, str(rand_id)) # Get file from url
                    if codeContent
                except: # If the url is invalid, send error message
                    await bot.send_message(message.channel, "```diff\n- Invalid URL File: \""+url.strip()+"\"\n```")
                    return
            else:
                await bot.send_message(message.channel, "```diff\n- Invalid URL File: \""+url.strip()+"\"\n```")
                return
     
     
        # Make sure the user isn't trying to use image only mode, because this is necessary for the bot's functionality
        if "--imagemode" in message_content:
            response = "Unable to process request, you are not allowed to use the `--imagemode` option"
        # Else start executing the program
        else:
            await bot.send_message(message.channel, "Started `astro8` with arguments: \"" + "".join(message_content.split()[1:]) + "\"\n\n ***Now please provide a file OR url to execute in this instance:***")
            msg = await bot.wait_for_message(timeout= 30, author=message.author, check=check)
            if msg is None:
                await bot.send_message(message.channel, "```diff\n- No input file or URL provided\n```")
                return

            # Run the astro8 emulator
            programOutput = subprocess.run(['~/Code/Astro8-Computer/Astro8-Emulator/linux-build/astro8', message_content.split()[1:]], stdout=subprocess.PIPE).stdout.decode('utf-8')
        

    await ctx.channel.send(response)

bot.run(token)
