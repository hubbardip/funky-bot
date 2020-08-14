import os
import discord
from dotenv import load_dotenv
import language_check
import sys
from io import StringIO
import compile_code

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

tool = language_check.LanguageTool('en-US')

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
        """
        old_stdout = sys.stdout
        output = sys.stdout = StringIO()
        exec(prog)
        sys.stdout = old_stdout
        """
        output = compile_code.comp(prog)
        if output[0] == "ok":
            print("hello")
            await message.channel.send(output[1])
        else:
            await message.channel.send(f"Error: {output[1]}")
    
    
    matches = tool.check(message.content)

    response = ""
    ignored_categories = ["Capitalization"]
    for match in matches:
        tox = match.tox
        fromx = match.fromx
        
        if match.category == "Possible Typo":
            word = message.content[fromx:tox]
            replacements = []
            for r in match.replacements:
                if r.lower() != word.lower():
                    replacements.append(r)

            if len(match.replacements) > 0 and len(replacements) == 0:
                add_res = False
            
            if len(replacements) > 0:
                response += f"Did you mean one of these: {', '.join(replacements)}\n"

    if response != "":
        await message.channel.send(response)

client.run(TOKEN)
