import os
import random
import uuid

import discord
from discord.ext import commands


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
    # Make sure the user isn't trying to use image only mode, because this is necessary for the bot's functionality
    if "--imagemode" in args:
        response = "Unable to process request, you are not allowed to use the `--imagemode` option"
    else:
        await bot.send_message(message.channel, "```diff\n- No input file provided\n```")
        msg = await bot.wait_for_message(timeout= 30, author=message.author, check=check)
        if msg is None:
            await bot.send_message(message.channel, "```diff\n- No input file provided\n```")
            return
      
        # Create random ID for this program
        rand_id = str(uuid.uuid1())
        print("Process with uuid: \"" + rand_id + "\" started.")
        # Run the astro8 emulator
  	    subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        

    await ctx.channel.send(response)

bot.run(token)
