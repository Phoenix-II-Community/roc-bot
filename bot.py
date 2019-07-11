#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import datetime
import settings
import discord
import logging
import fuzzywuzzy
from fuzzywuzzy import process
from discord.utils import get
from discord.ext import commands
import json
from pathlib import Path

home_dir = Path.home()

# Open the required json files and assign it to a variable foo_data
ships_json = open(('{hd}/scripts/apex-bot/res/ships.json').format(hd=home_dir))
ships_data = json.load(ships_json)
invaders_json = open(('{hd}/scripts/apex-bot/res/invaders.json').format(hd=home_dir))
invaders_data = json.load(invaders_json)
emoji_json = open(('{hd}/scripts/apex-bot/res/emoji.json').format(hd=home_dir))
emoji_data = json.load(emoji_json)


embed_colours = {"sb": 0x3a77f9, "hi": 0xee4529, "ap": 0xffb820}

logging.basicConfig(level=logging.INFO)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

##############
### Functions
##############

# return the ship name from ships_data using the last value
# the last value is the ship name 
def ship_search(find_this):
    found_this = process.extractOne(find_this, ships_data)
    ship_name = found_this[-1]
    return ship_name

# Use the slutty ship_search function to return the ship name key which flies 
# in the face of how a dict is meant to work. The stat_name is provided from the
# get_ship_description_small function or similar. 
def ship_stat(find_ship, stat_name):
    stat_value = ships_data[ship_search(find_ship)][stat_name]
    return stat_value

# Discord embed have a line of the left hand side. This line can be coloured
# This function uses one of the 3 damage_type choices to select a colour from
# the embed_colours variable (red/yellow/blue)
def get_em_colour(arg1):
    dmg_type = ship_stat(arg1, "damage_type")
    em_colour = embed_colours[dmg_type]
    return em_colour

# This is the small embed description output used by the
#  "!ship info <ship name>" command. 
def get_ship_description_small(arg1):
    ship_description_small = ("{emojidps} {dpsvalue}\n"
    "{emojidmgtype} {weaponname}\n"
    "{emojiaura} {auraname}\n"
    "{emojizen} {zenname}\n").format(emojidps=emoji("dps"),
            dpsvalue=str(ship_stat(arg1, "damage_output")),
            emojidmgtype=emoji(ship_stat(arg1, "damage_type")),
            weaponname=(ship_stat(arg1, "weapon_name")),
            emojiaura=emoji(ship_stat(arg1, "aura")),
            auraname=ship_stat(arg1, "aura"),
            emojizen=emoji(ship_stat(arg1, "zen")),
            zenname=ship_stat(arg1, "zen"))
    return ship_description_small

# Creates the title of the discord emebed consisting of the rarity emoji 
# the ship name.
def get_ship_title(arg1):
    ship_title = ("{rarityemoji} {nameofship}").format(\
        rarityemoji=emoji(ship_stat(arg1, "rarity")), 
        nameofship=ship_stat(arg1, "ship_name"))
    return ship_title

# Receives the element from ships.json maybe another file in 
# future and uses it as a key in emoji.json.
def emoji(key):
    emoji = emoji_data[key]
    return emoji

def get_ship_image(arg1):
    urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/img/"
    url = ("{giturl}{shipname}.png").format(giturl=urlgit, shipname=ship_search(arg1))
    return url

################
### Bot commands
################

client = MyClient()
bot = commands.Bot(command_prefix="!")


# quick countodwn hack until Phoenix II Birthday on 2019 June 28
@bot.command()
async def bday(ctx):
    if ctx.invoked_subcommand is None:
        present = datetime.datetime.now()
        future = datetime.datetime(2019, 7, 28, 0, 0, 0)
        difference = future - present
        print(str(difference))
        print(str(difference)[0])
        await ctx.send(difference)


@bot.group()
async def ship(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid ship command passed.')

# Sub command to the @bot.group() decorator ship function.
# Intended that for use in high traffic channels, the output size is intential small.
# A 5 line embed with basic info: name, weapon, dps, aura and zen.
@ship.command()
async def info(ctx, *, arg1):
    ship_embed_title = get_ship_title(arg1)
    ship_embed_description = get_ship_description_small(arg1)
    embed_colour = get_em_colour(arg1)
    embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
    embed.set_thumbnail(url=get_ship_image(arg1))
    await ctx.send(embed=embed)
    return

#@info.error
#async def info_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send('nothing to see here comrade.')

# If a message receives the :el: emoji, then the bot should add it's own :el: reaction
@bot.event
async def on_reaction_add(reaction, user):
    # we do not want the bot to react to its own reaction
    if user == bot.user:
        return
    if str(reaction.emoji) == "<:el:373097097727049728>":
        emoji = get(bot.emojis, name='el')
        await reaction.message.add_reaction(emoji)
        return

# If someone uses the :el: emoji in a message then the bot should add it's own :el: reaction to the message.
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if ':el:' in message.content:
        emoji = get(bot.emojis, name='el')
        await message.add_reaction(emoji)
        return

bot.run(settings.discordkey)
