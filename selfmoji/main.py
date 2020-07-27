import os
import re
from configparser import ConfigParser
from typing import Optional

import crayons
from discord.ext import commands

TOKEN_ENV_KEY = "DISCORD_TOKEN"
TOKEN_FILE = "TOKEN"
EMOJI_FILE = "emojis.dict"
CONFIG_FILE = "config.ini"
SIZES = {16, 32, 64, 128, 256, 512}

bot = commands.Bot(command_prefix="``", self_bot=True)

emojis = {}

config_parser = ConfigParser()

config_parser["selfmoji"] = {"size": "64", "edit": "yes"}


def to_int(s: str) -> int:
    try:
        i = int(s)
    except:
        raise ValueError(f"[{s}] is not a number")
    if i in SIZES:
        return i
    raise ValueError(f"[{s}] is not in {SIZES}")


def config(attr: Optional[str] = None):
    if attr:
        return config_parser["selfmoji"][attr]
    return config_parser["selfmoji"]


def save_emojis():
    with open(EMOJI_FILE, "w") as file:
        for k, v in emojis.items():
            file.write(f"{k} : {v}\n")


def read_emojis():
    try:
        with open(EMOJI_FILE, "r") as file:
            for line in file:
                k, v = line.strip().split(" : ")
                emojis[k] = v
    except FileNotFoundError:
        raise EnvironmentError(f"File [{EMOJI_FILE}] does not exist, not loading")


def save_config():
    with open(CONFIG_FILE, "w") as file:
        config_parser.write(file)


def read_config():
    if os.path.isfile(CONFIG_FILE):
        config_parser.read(CONFIG_FILE)
    else:
        raise EnvironmentError(f"File [{CONFIG_FILE}] does not exist, not loading")


def token() -> str:
    if tok := os.getenv(TOKEN_ENV_KEY):
        print(crayons.green("Loading token from environment"))
        return tok
    if os.path.isfile(TOKEN_FILE):
        print(crayons.green("Loading token from file"))
        with open(TOKEN_FILE, "r") as file:
            return file.read().strip()
    raise ValueError("Could not get token")


def main():

    print(crayons.green("Starting"))

    try:
        read_config()

        print(crayons.green("Read config file"))
    except EnvironmentError as enve:
        print(crayons.yellow(enve))
        print(crayons.yellow("Using defaults..."))

    print(crayons.green(f"Emoji size: [{config().getint('size')}]"))

    print(
        crayons.green(
            f"Message editing is {'enabled' if config().getboolean('edit') else 'disabled'}"
        )
    )

    try:
        read_emojis()

        print(crayons.green(f"Loaded [{len(emojis)}] emojis"))

        print(crayons.cyan(str(list(emojis.keys()))))
    except EnvironmentError as enve:
        print(crayons.yellow(enve))

    try:
        bot.run(token(), bot=False)
    finally:
        print(crayons.red("SAVING EMOJIS"))
        save_emojis()
        print(crayons.red("SAVING CONFIG"))
        save_config()


@bot.command()
async def flush(ctx):
    try:
        save_emojis()
        print(crayons.green("Saved emojis"))
    finally:
        await ctx.message.delete()


@bot.command()
async def add(ctx, name, link):
    try:
        print(crayons.yellow(f"Registering emoji [{name}] with [{link}]"))
        emojis[name.strip()] = re.sub(r"&size=\d{2,3}", "", link.strip())
    finally:
        await ctx.message.delete()


@bot.command()
async def delete(ctx, name):
    try:
        name = name.strip()
        if name in emojis:
            print(crayons.yellow(f"Deleting emoji [{name}]"))
            del emojis[name.strip()]
        else:
            print(crayons.red(f"There is no emoji named [{name}]"))
    finally:
        await ctx.message.delete()


@bot.command()
async def rename(ctx, original, newname):
    try:
        original = original.strip()
        newname = newname.strip()
        if newname in emojis:
            print(crayons.red(f"Emoji [{newname}] already exists!"))
        elif original in emojis:
            print(crayons.yellow(f"Renaming emoji [{original}] to [{newname.strip()}]"))
            emojis[newname.strip()] = emojis[original]
            del emojis[original]
        else:
            print(crayons.red(f"There is no emoji named [{original}]"))
    finally:
        await ctx.message.delete()


@bot.command()
async def size(ctx, _size: Optional[str] = None):
    if _size:
        try:
            __size = to_int(size)
            print(crayons.yellow(f"Setting emoji size to {__size}"))
            config()["size"] = __size
        except ValueError as ve:
            print(crayons.red(f"Error parsing input: {ve}"))
        finally:
            await ctx.message.delete()
    else:
        await ctx.send(f"Emoji size is `[{config('size')}]`")


@bot.command()
async def edit(ctx, opt: Optional[bool] = None):
    try:
        if opt is None:
            if config().getboolean("edit"):
                config()["edit"] = "no"
            else:
                config()["edit"] = "yes"
        else:
            if opt:
                config()["edit"] = "yes"
            else:
                config()["edit"] = "no"
    finally:
        print(crayons.cyan(f"Changed edit to [{config().getboolean('edit')}]"))
        await ctx.message.delete()


@bot.command(aliases=["list"])
async def _list(ctx):
    await ctx.message.edit(
        content=f"There are `[{len(emojis)}]` emojis: ```{', '.join(emojis.keys())}```"
    )


@bot.command()
async def slist(ctx):
    try:
        print(
            crayons.cyan(
                f"There are [{len(emojis)}] emojis: {', '.join(emojis.keys())}"
            )
        )
    finally:
        await ctx.message.delete()


@bot.event
async def on_command_error(ctx, error):
    print(crayons.red(error))


@bot.event
async def on_ready():
    print(crayons.green("ready!"))


@bot.event
async def on_message(message):
    if message.author != bot.user:
        return

    async def do_emoji(content, _size=None):

        if content not in emojis:
            return

        if not _size:
            _size = config().getint("size")

        emoji = emojis[content] + f"&size={_size}"

        if config().getboolean("edit"):

            await message.edit(content=emoji)

        else:

            await message.delete()

            await message.channel.send(emoji)

    content = message.content.strip()

    if match := re.match(r"`(\w+) (\d+)`", content):
        try:
            await do_emoji(match.group(1), to_int(match.group(2)))
        except Exception as e:
            if isinstance(e, ValueError):
                print(crayons.red(f"Error parsing input: {e}"))
            else:
                print(crayons.red(f"Unknown exception: {e}"))
            await message.delete()
    elif match := re.match(r"`([\w ]+)`", content):
        await do_emoji(match.group(1))
    else:
        await bot.process_commands(message)


if __name__ == "__main__":
    main()
