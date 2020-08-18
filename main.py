import os
import discord
from dotenv import load_dotenv
import sys
from io import StringIO
import compile_code

load_dotenv()
TOKEN = "NzQyNTQ1NzcwODAwMDg3MTAw.XzHrow.ganMphJrM2AHNvLzhYjp2e0QSSo"
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

    
    if message.content[:8] == "+compile":
        
        prog_lang = message.content[9:]
        prog = " ".join(prog_lang.split(" ")[1:])
        lang = prog_lang.split(" ")[0]
        output = compile_code.comp(lang, prog)
        if output[0] == "ok":
            print("hello")
            await message.channel.send(output[1])
        else:
            await message.channel.send(f"Error: {output[1]}")
    

client.run(TOKEN)
