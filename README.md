# Selfmoji

![video](https://i.imgur.com/Jf1kGKm.gif)

Do you like Discord? Do you like using emojis? Do you not like paying for Nitro:tm:?

With selfmoji you can have your own custom emojis in Discord.

Warning: This operates through a selfbot which is against the Discord ToS

## Installing

1. Clone repository
2. `pipenv sync`
3. Supply your token:

    3.0 How do I get my token?: [Guide](https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs)

    3.1 Place your token in a file named `TOKEN`

    3.2 Create an environment variable `DISCORD_TOKEN`

    3.3 Place it in the config file

      - Bot will prompt you on first run

4. Run the appropriate run script

## Sending emojis

send `` `[emoji-name]` `` or `` `[emoji-name] [size]` `` where `[size]` is one of `16, 32, 64, 128, 256`

e.g. `` `weirdchamp` `` or `` `weirdchamp 256` ``

Send the `weirdchamp` emoji, first using the currently configured size, second explicitly using size `256`

If editing is enabled the bot will edit the message to be the desired emote, if editing is disabled the bot will delete the message and send a new one with the emote

If using the first form, the bot uses the currently configured size

## How Does it Work?

Selfmoji is a self-bot, it listens to your messages and acts accordingly. The bot links a discord emoji and sets the size using a URL parameter.

## The Problem with Mobile

~~In classic Discord:tm: fashion mobile doesn't handle this particularly well, while desktop Discord will size the emotes properly mobile finds the need to increase the size arbitrarily.~~

They fixed it!

## Share Emojis

Selfmoji saves emoji in a file called `emojis.dict` in the format `emoji-name : link`

You can add emojis here manually and share with friends

## Migrating The Emojis File

Selfmoji has recently been updated to store its emojis in a different format

If your file looks like:

```
[emoji-name] : https://cdn.discordapp.com/emojis/...
...```

Then please migrate to the new scheme using the included tool: `pipenv run python selfmoji/migrate.py [your-emojis-file]`

## Commands

The bot uses the prefix `` as it's not likely to collide with anything else

### Add Emoji

``` ``add [emoji-name] [emoji-link] ```

e.g. ``` ``add sparklecat https://cdn.discordapp.com/emojis/654099753340239872.gif ```

![laugh](https://i.imgur.com/fuCfyS2.gif)

### Delete Emoji

``` ``remove [emoji-name] ```

``` ``delete [emoji-name] ```

### Rename Emoji

``` ``rename [current-name] [new-name] ```

``` ``move [current-name] [new-name] ```

### List Available Emoji

``` ``list ```

``` ``search ```

> Sends a message into the current chat listing all the emojis

``` ``list|search pog ```

> Sends a message into the current chat with all emojis matching the search "pog"

``` ``slist ```

``` ``ssearch ```

> **S**ilent list, sends a list of all emoji into the console

``` ``slist|ssearch pog ```

> Sends a message into the console with all emojis matching the search "pog"

### Set Emoji Size

``` ``size [pixel-size] ```

Where `[pixel-size]` is one of `16, 32, 64, 128, 256, 512`

### Get the current size

``` ``size ```

> Sends a message to the current chat

### Enable / Disable Message Editing

``` ``edit [true|yes|on] ```

> Enables editing

``` ``edit [false|no|off] ```

> Disables editing

### Get Editing Status

``` ``edit ```

> Sends a message to the current chat


### Enable / Disable Autoflush

``` ``autoflush [true|yes|on] ```

``` ``autoflush [false|no|off] ```

> Autoflushing saves the emojis file every time you add / delete / rename emojis

### Get Autoflush Status

``` ``autoflush ```

> Sends a message to the current chat