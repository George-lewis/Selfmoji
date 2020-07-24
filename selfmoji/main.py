import discord, crayons, os, re
from discord.ext import commands
from configparser import ConfigParser

bot = commands.Bot(command_prefix="``", self_bot=True)

emoji = {}

config = ConfigParser()

def save_emojis():
    with open('emojis.dict', 'w') as file:
        for k, v in emoji.items():
            file.write(f"{k} : {v}\n")

def read_emojis():
    with open('emojis.dict', 'r') as file:
        for line in file:
            k, v = line.strip().split(' : ')
            emoji[k] = v

def token() -> str:
    if token := os.getenv('DISCORD_TOKEN'):
        print(crayons.green("Loading token from environment"))
        return token
    elif os.path.isfile('TOKEN'):
        print(crayons.green("Loading token from file"))
        with open('TOKEN', 'r') as file:
            return file.read().strip()
    else:
        raise ValueError("Bruh")

def main():

    print(crayons.green("Starting"))

    config.read("config.ini")

    print(crayons.green("Read config file"))

    read_emojis()

    print(crayons.green(f"Loaded [{len(emoji)}] emojis"))

    print(list(emoji.keys()))

    try:
        bot.run(token(), bot=False)
    finally:
        print(crayons.red("SAVING EMOJIS"))
        save_emojis()

@bot.command()
async def add(ctx, name, link):
    print(crayons.yellow(f"Registering emoji [{name}] with [{link}]"))
    emoji[name.strip()] = link.strip()
    await ctx.message.delete()

@bot.event
async def on_ready():
    print(crayons.green("ready!"))

@bot.event
async def on_message(message):
    if message.author != bot.user:
        return
    
    if not re.match("`.+`", message.content):
        await bot.process_commands(message)
        return

    content = message.content.strip().replace("`", "").strip()

    if content not in emoji:
        return

    e = emoji[content] + "&size=32"

    if config['selfmoji'].getboolean('edit'):

        await message.edit(content=e)

    else:

        await message.delete()

        await message.channel.send(e)

if __name__ == "__main__":
    main()