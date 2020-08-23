import os, re, logging
from typing import Optional

from config import Config
from utils import setup_logging

import crayons
from discord.ext import commands

TOKEN_ENV_KEY = "DISCORD_TOKEN"
TOKEN_FILE = "TOKEN"
EMOJI_FILE = "emojis.dict"
CONFIG_FILE = "config.json"
SIZES = {16, 32, 64, 128, 256}

setup_logging()

logger = logging.getLogger("MAIN")

logger.setLevel(logging.INFO)

config = Config(CONFIG_FILE)

config.load()

logger.info(f"Emoji size: [{config.size}]")

logger.info(f"Message editing is {'enabled' if config.edit else 'disabled'}")

logger.info(f"Autoflush is {'enabled' if config.autoflush else 'disabled'}")

bot = commands.Bot(command_prefix=config.prefix, self_bot=True)

emojis = {}


def to_int(s: str) -> int:
    try:
        i = int(s)
    except:
        raise ValueError(f"[{s}] is not a number")
    if i in SIZES:
        return i
    raise ValueError(f"[{s}] is not in {SIZES}")


def save_emojis():
    with open(EMOJI_FILE, "w") as file:
        for k, v in emojis.items():
            file.write(f"{k} : {v}\n")
    logger.info("Saved emojis")


def read_emojis():
    try:
        with open(EMOJI_FILE, "r") as file:
            for line in file:
                k, v = line.strip().split(" : ")
                emojis[k] = v
    except FileNotFoundError:
        raise EnvironmentError(f"File [{EMOJI_FILE}] does not exist, not loading")


def token() -> str:
    if tok := config.token:
        logger.info("Loading token from config file")
        return tok
    if tok := os.getenv(TOKEN_ENV_KEY):
        logger.info("Loading token from environment")
        return tok
    if os.path.isfile(TOKEN_FILE):
        logger.info("Loading token from file")
        with open(TOKEN_FILE, "r") as file:
            return file.read().strip()
    raise ValueError("Could not get token")


def main():

    logger.info("Starting")

    try:
        read_emojis()

        logger.info(f"Loaded [{len(emojis)}] emojis")

        print(crayons.cyan(list(emojis.keys())))
    except EnvironmentError as enve:
        logger.warning(enve)

    try:
        bot.run(token(), bot=False)
    finally:
        logger.info("SAVING EMOJIS")
        save_emojis()
        logger.info("SAVING CONFIG")
        config.save()


@bot.command()
async def flush(ctx):
    try:
        save_emojis()
    finally:
        if ctx:
            await ctx.message.delete()


@bot.command()
async def add(ctx, name, link):
    try:
        logger.info(f"Registering emoji [{name}] with [{link}]")
        emojis[name.strip()] = re.sub(r"&size=\d{2,3}", "", link.strip())
    finally:
        await ctx.message.delete()
    if config.autoflush:
        save_emojis()


@bot.command(aliases=["remove"])
async def delete(ctx, name):
    try:
        name = name.strip()
        if name in emojis:
            logger.info(f"Deleting emoji [{name}]")
            del emojis[name.strip()]
        else:
            logger.error(f"There is no emoji named [{name}]")
    finally:
        await ctx.message.delete()
    if config.autoflush:
        save_emojis()


@bot.command(aliases=["move"])
async def rename(ctx, original, newname):
    try:
        original = original.strip()
        newname = newname.strip()
        if newname in emojis:
            logger.warning(f"Emoji [{newname}] already exists!")
        elif original in emojis:
            logger.warning(f"Renaming emoji [{original}] to [{newname.strip()}]")
            emojis[newname.strip()] = emojis[original]
            del emojis[original]
        else:
            logger.error(f"There is no emoji named [{original}]")
    finally:
        await ctx.message.delete()


@bot.command()
async def size(ctx, _size: Optional[str] = None):
    if _size:
        try:
            # Todo: __size is unused
            __size = to_int(_size)
            logger.warning(f"Setting emoji size to {__size}")
            config.size = _size
        except ValueError as ve:
            logger.error(f"Error parsing input: {ve}")
        finally:
            await ctx.message.delete()
    else:
        await ctx.message.edit(content=f"Emoji size is `[{config.size}]`")


@bot.command()
async def autoflush(ctx, opt: Optional[bool] = None):
    def text():
        return "enabled" if config.autoflush else "disabled"

    if opt is None:
        await ctx.message.edit(content=f"Autoflush is `[{text()}]`")
    else:
        config.autoflush = opt

        logger.info(f"{text().capitalize()} autoflush")

        await ctx.message.delete()


@bot.command()
async def edit(ctx, opt: Optional[bool] = None):
    def text():
        return "enabled" if config.edit else "disabled"

    if opt is None:
        await ctx.message.edit(content=f"Editing is `[{text()}]`")
    else:
        config.edit = opt
        logger.info(f"{text().capitalize()} editing")
        await ctx.message.delete()


def search_emojis(term: str = None) -> str:
    if term:
        keys = emojis.keys()
        if (matches := [key for key in keys if term in key]) :
            return f"There are `[{len(matches)}]` emojis matching the search `[{term}]`: ```{', '.join(matches)}```"
        return "No matches"

    return f"There are `[{len(emojis)}]` emojis: ```{', '.join(emojis.keys())}```"


@bot.command(aliases=["list", "search"])
async def _list(ctx, term: Optional[str]):
    await ctx.message.edit(content=search_emojis(term))


@bot.command(aliases=["ssearch"])
async def slist(ctx, term: Optional[str]):
    try:
        print(crayons.cyan(search_emojis(term)))
    finally:
        await ctx.message.delete()


@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command Error: {error}")


@bot.event
async def on_connect():
    logger.info("Connected")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        return

    async def do_emoji(content, _size=None):

        if content not in emojis:
            return

        if not _size:
            _size = config.size

        emoji = emojis[content] + f"&size={_size}"

        if config.edit:

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
                logger.error(f"Error parsing input: {e}")
            else:
                logger.error(f"Unknown exception: {e}")
            await message.delete()
    elif match := re.match(r"`([\w ]+)`", content):
        await do_emoji(match.group(1))
    else:
        await bot.process_commands(message)


if __name__ == "__main__":
    main()
