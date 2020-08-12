import os
import discord
from dotenv import load_dotenv
import sys
from io import StringIO

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(f"{client.user} has connected to Discord!")
    print(f"{guild.name}(id: {guild.id})")

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    #print(message.content)

    
    if "/compile" in message.content:
        prog = message.content[9:]

        old_stdout = sys.stdout
        red_output = sys.stdout = StringIO()
        exec(prog)
        sys.stdout = old_stdout
        await message.channel.send(red_output.getvalue())
    

client.run(TOKEN)
