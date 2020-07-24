import os
import re
from configparser import ConfigParser
from typing import Optional

import crayons
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="``", self_bot=True)

emoji = {}

config = ConfigParser()


def save_emojis():
    with open("emojis.dict", "w") as file:
        for k, v in emoji.items():
            file.write(f"{k} : {v}\n")


def read_emojis():
    with open("emojis.dict", "r") as file:
        for line in file:
            k, v = line.strip().split(" : ")
            emoji[k] = v


def save_config():
    with open("config.ini", "w") as file:
        config.write(file)


def read_config():
    config.read("config.ini")


def token() -> str:
    if token := os.getenv("DISCORD_TOKEN"):
        print(crayons.green("Loading token from environment"))
        return token
    elif os.path.isfile("TOKEN"):
        print(crayons.green("Loading token from file"))
        with open("TOKEN", "r") as file:
            return file.read().strip()
    else:
        raise ValueError("Bruh")


def main():

    print(crayons.green("Starting"))

    read_config()

    print(crayons.green("Read config file"))

    print(crayons.green(f"Emoji size: [{config['selfmoji'].getint('size')}]"))

    print(
        crayons.green(
            f"Message editing is {'enabled' if config['selfmoji'].getboolean('edit') else 'disabled'}"
        )
    )

    read_emojis()

    print(crayons.green(f"Loaded [{len(emoji)}] emojis"))

    print(crayons.cyan(str(list(emoji.keys()))))

    try:
        bot.run(token(), bot=False)
    finally:
        print(crayons.red("SAVING EMOJIS"))
        save_emojis()
        print(crayons.red("SAVING CONFIG"))
        save_config()


@bot.command()
async def add(ctx, name, link):
    print(crayons.yellow(f"Registering emoji [{name}] with [{link}]"))
    emoji[name.strip()] = link.strip()
    await ctx.message.delete()


@bot.command()
async def delete(ctx, name):
    name = name.strip()
    if name in emoji:
        print(crayons.yellow(f"Deleting emoji [{name}]"))
        del emoji[name.strip()]
    else:
        print(crayons.red(f"There is no emoji named [{name}]"))
    await ctx.message.delete()


@bot.command()
async def rename(ctx, orginal, newname):
    original = original.strip()
    if name in emoji:
        print(crayons.yellow(f"Renaming emoji [{original}] to [{newname.strip()}]"))
        emoji[newname.strip()] = emoji[original]
        del emoji[original]
    else:
        print(crayons.red(f"There is no emoji named [{original}]"))
    await ctx.message.delete()


@bot.command()
async def size(ctx, size: Optional[str]):
    if size:
        try:
            _size = int(size)
            if _size % 2 == 0:
                print(crayons.yellow(f"Setting emoji size to {size}"))
                config["selfmoji"]["size"] = size
            else:
                print(crayons.red(f"[{size}] is not a power of two"))
        except:
            print(crayons.red(f"[{size}] is not a number"))
        await ctx.message.delete()
    else:
        await ctx.send(f"Emoji size is [{config['selfmoji']['size']}]")


@bot.command(aliases=["list"])
async def _list(ctx):
    # await ctx.message.delete()
    await ctx.send(f"There are `[{len(emoji)}]` emojis: `{list(emoji.keys())}`")


@bot.event
async def on_ready():
    print(crayons.green("ready!"))


@bot.event
async def on_message(message):
    if message.author != bot.user:
        return

    if not re.match("`\w+`", message.content):
        await bot.process_commands(message)
        return

    content = message.content.strip().replace("`", "").strip()

    if content not in emoji:
        return

    e = emoji[content] + f"&size={config['selfmoji'].getint('size')}"

    if config["selfmoji"].getboolean("edit"):

        await message.edit(content=e)

    else:

        await message.delete()

        await message.channel.send(e)


if __name__ == "__main__":
    main()
