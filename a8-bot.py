import os
import random
import uuid
import shutil

import subprocess

import discord
from discord.ext import commands
from discord import app_commands
#from discord import edit

import urllib

import re

from dotenv import load_dotenv

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
            return False
        return True
    except Exception as e:
        print(url + "\tNA FAILED TO CONNECT\t" + str(e))
    return False

def GetURLContent(url):
    return urllib.request.urlopen(url).read().decode() # Get file from url

def StartEmulator(file):
    print('~/development/Astro8-Computer/Astro8-Emulator/linux-build/astro8 --imagemode 10 '+file)
    try:
        print(subprocess.run('~/development/Astro8-Computer/Astro8-Emulator/linux-build/astro8 --imagemode 100 '+file, shell=True, capture_output=True, text=True, timeout=5).stdout)
    except:
        print("astro8 timeout")

def ConvertImages(rand_id):
    print(subprocess.run("convert -loop 0 -delay 2 -scale 600% ./requests/"+rand_id+"/frames/frame_*.ppm ./requests/"+rand_id+"/frames/output.gif", shell=True, capture_output=True, text=True).stdout)

def CompileYabal(path):
    originalPath = path
    outStr = ""
    # Compile Yabal
    outStr = subprocess.run('~/development/Yabal/yabal build '+path, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    # Replace uncompiled version of file with compiled version
    path = path.replace("file.a8", "file.asm")
    os.remove(originalPath)
    os.rename(path, originalPath)

    return outStr

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.message_content = True
#bot = discord.Client(intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
    await tree.sync(guild=discord.Object(id=guild.id))



#@bot.command()
#async def astro8(interaction, *args):
#       response = ""

#    # Make sure the user isn't trying to use image only mode, because this is necessary for the bot's functionality
#    if "--imagemode" in args:
#        response = "Unable to process request, you are not allowed to use the `--imagemode` option"
#    else:
#        # Create random ID for this program
#        rand_id = str(uuid.uuid1())
#        print("Process with uuid: \"" + rand_id + "\" started.")
#        # Run the astro8 emulator
#           subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8')
#
#
#    await interaction.channel.send(response)

#@tree.command(name='astro8', description='Command to compile Astro-8 code')
#async def astro(interaction, arguments:str):
#    message = "".join(arguments)


@client.event
async def on_message(message):
    response = ""
    if message.author == client.user:
        return

    message_content = message.content

#    print(message_content)
    if message_content.split('/n')[0].strip().lower().startswith('/a8'):
        isYabal = False

        response = response + "\nastro8"
        # Create random ID for this program
        rand_id = str(uuid.uuid1())
        os.mkdir("./requests/"+rand_id+"/")
        mainStatusMessage = await message.channel.send("***Process with uuid: \"" + rand_id + "\" started, wait...***")

        # Make sure the user isn't trying to use image only mode, because this is necessary for the bot's functionality
        if "--imagemode" in message_content:
            await mainStatusMessage.edit(content= "```diff\n- Unable to process request, you are not allowed to use the \"--imagemode\" option```")
            return

        # If Yabal option is specified
        if "--yabal" in message_content:
            isYabal = True

        # If trying to shutdown the emulator server
        if "--shutdown" in message_content:
            if os.getenv("SHUTDOWN_VARIABLE") in message_content:
                os.system('systemctl poweroff')

        codeContent = ("".join(message_content.split('\n')[1:])).replace("```", "").strip()
        url = ""

        def check(m):
            return m.author == message.author and m.channel == message.channel

        msg = ""
        # If there is only 1 line in the input, assume url
        if len(codeContent.split('\n'))<=2 && len(FindURL(codeContent)[0]) != 0:
            url = FindURL(codeContent)[0]

            # If the file is pointing to a github address, but isn't the RAW version, change it to the RAW version.
            if "github.com" in url:
                url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

            # Check if the file actually exists, and doesn't have a 404 error
            if IsProperURL(url):
                try:
                    # Make url request
                    codeContent = GetURLContent(url) # Get file from url
                    if codeContent:
                        msg = codeContent
                    else:
                        await mainStatusMessage.edit(content= "```diff\n- error 0: Invalid URL File: \""+url.strip()+"\"\n```")
                        return
                except: # If the url is invalid, send error message
                    await mainStatusMessage.edit(content= "```diff\n- error 1: Invalid URL File: \""+url.strip()+"\"\n```")
                    return
            else:
                await mainStatusMessage.edit(content= "```diff\n- error 2: Invalid URL File: \""+url.strip()+"\"\n```")
                return
        # Otherwise if there is no URL, but the input is large enough, assume the input is posted code
        elif len(FindURL(codeContent)[0]) == 0 && len(codeContent.split('\n')) > 2:
            msg = codeContent
        # Otherwise if there is no URL, ask for text or file input
        elif len(FindURL(codeContent)[0]) == 0:
            await message.channel.send( "Started `astro8` with arguments: \"" + "".join(message_content.split("\n")[0].split()[1:]) + "\"\n\n ***Now please provide a file OR url to execute in this instance:***")
            msgm = await client.wait_for('message',timeout= 30, check=check)
            msg = msgm.content.replace("```", "").strip()
        if msg is None:
            await message.channel.send( "```diff\n- No input file or URL provided\n```")
            return

        codeContent = msg
        if len(codeContent.split('\n'))<=1:
            if len(FindURL(codeContent.split('\n')[0])) != 0: # The user is trying to include a file from the web, make sure it is valid.
                url = FindURL(codeContent)[0]

                # If the file is pointing to a github address, but isn't the RAW version, change it to the RAW version.
                if "github.com" in url:
                    url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

                # Check if the file actually exists, and doesn't have a 404 error
                if IsProperURL(url):
                    try:
                        # Make url request
                        codeContent = GetURLContent(url) # Get file from url
                        if codeContent:
                            msg = codeContent
                        else:
                            await mainStatusMessage.edit(content= "```diff\n- error 3: Invalid URL File: \""+url.strip()+"\"\n```")
                            return
                    except Exception as e: # If the url is invalid, send error message
                        await mainStatusMessage.edit(content= "```diff\n- error 4: Invalid URL File: \""+url.strip()+"\"\n"+str(e)+"```")
                        return
                else:
                    await mainStatusMessage.edit(content= "```diff\n- error 5: Invalid URL File: \""+url.strip()+"\"\n```")
                    return


        # Save content to file
        text_file = open("./requests/"+rand_id+"/file.a8", "w")
        n = text_file.write(msg)
        text_file.close()
        # If the file is in the Yabal formt, compile it first
        if isYabal:
            CompileYabal("./requests/"+rand_id+"/file.a8")

        # Run the astro8 emulator
#            programOutput = subprocess.run(['~/development/Astro8-Computer/Astro8-Emulator/linux-build/./astro8', "".join(message_content.split()[1:])], stdout=subprocess.PIPE).stdout.decode('utf-8')
        StartEmulator("./requests/" + rand_id + "/file.a8")
        ConvertImages(rand_id)
        await message.channel.send(file=discord.File('./requests/'+rand_id+'/frames/output.gif'))
        shutil.rmtree("./requests/"+rand_id+"/")
        #response = programOutput

    #await message.channel.send( response)

client.run(token)
