#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import datetime
import settings
import discord
import logging
import fuzzywuzzy
from fuzzywuzzy import fuzz
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


embed_colours = {"Shield Breaker": 0x3a77f9, "High Impact": 0xee4529, "Armor Piercing": 0xffb820}
aura_list = ["Bullet EMP", "Stun EMP", "Barrier", "Laser Storm", \
    "Missile Swarm", "Point Defence", "Chrono Field", "Vorpal Lance", \
    "Phalanx", "Ion Cannon","Goliath Missile", "Blade Storm"]

zen_list = ["Kappa Drive", "Mega Laser", "Mega Bomb", "Teleport", "Reflex EMP",\
    "Personal Shield", "Tracking Minigun", "Focus Lance", \
        "Trinity Teleport", "Nightfury"]

wpn_dmg_list = ["High Impact", "Armor Piercing", "Shield Breaker"]


logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("Phoenix II")
    await bot.change_presence(status=discord.Status.online, activity=game)

################################################################
####                         Functions                      ####
################################################################

# return the ship name from ships_data using the last value
# the last value is the ship name 
def ship_search(find_this):
    found_this = process.extractOne(find_this, ships_data.keys())
    ship_name = found_this[0]
    return ship_name

# Use the slutty ship_search function to return the ship name key which flies 
# in the face of how a dict is meant to work. The stat_name is provided from the
# get_ship_description_small function or similar. 
def ship_stat(find_ship, stat_name):
    ship_dict = ships_data[ship_search(find_ship)]
    return ship_dict

# Discord embed have a line of the left hand side. This line can be coloured
# This function uses one of the 3 damage_type choices to select a colour from
# the embed_colours variable (red/yellow/blue)
def get_em_colour(ship_name):
    ship_dict = ships_data[ship_name]
    dmg_type = ship_dict["damage_type"]
    em_colour = embed_colours[dmg_type]
    return em_colour

# Receives the element from ships.json maybe another file in 
# future and uses it as a key in emoji.json.
def emoji(key):
    emoji = emoji_data[key]
    return emoji

# This is the small embed description output used by the
#  "!ship info <ship name>" command. 
def get_ship_description_small(ship_name):
    ship_dict = ships_data[ship_name]
    print(ship_dict)
    ship_description_small = ("{emojidps} {ship[damage_output]}\n"
    "{emojidmgtype} {ship[weapon_name]}\n"
    "{emojiaura} {ship[aura]}\n"
    "{emojizen} {ship[zen]}\n").format(emojidps=emoji("dps"),
            emojidmgtype=emoji(ship_dict["damage_type"]),
            emojiaura=emoji(ship_dict["aura"]),
            emojizen=emoji(ship_dict["zen"]),
            ship=ship_dict)
    return ship_description_small

def find_number(ship_name):
    ship_dict = ships_data[ship_name]
    number = ship_dict["number"]
    return number

# Creates the title of the discord emebed consisting of the rarity emoji 
# the ship name.
def get_ship_title(ship_name):
    ship_dict = ships_data[ship_name]
    ship_title = ("{rarityemoji} {nameofship}").format(\
        rarityemoji=emoji(ship_dict["rarity"]), 
        nameofship=ship_dict["ship_name"])
    return ship_title

def get_ship_image(ship_name):
    urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/img/"
    url = ("{giturl}{shipname}.png").format(giturl=urlgit, shipname=ship_name)
    return url

def aura_search(find_this):
    list1 = []
    found_this = process.extractOne(find_this, aura_list)
    for elements in ships_data.values():
        if elements['aura'] == found_this[0]:
            list1.append(elements['ship_name'])
    return ', '.join(list1)

def zen_search(find_this):
    list1 = []
    found_this = process.extractOne(find_this, zen_list)
    for elements in ships_data.values():
        if elements['zen'] == found_this[0]:
            list1.append(elements['ship_name'])
    return ', '.join(list1)

def wpn_dmg_search(find_this):
    list1 = []
    if find_this == "ap":
        find_this = "Armor Piercing"
    elif find_this == "hi":
        find_this = "High Impact"
    elif find_this == "sb":
        find_this = "Shield Breaker"
    else:
        pass
    found_this = process.extractOne(find_this, wpn_dmg_list)
    for elements in ships_data.values():
        if elements['damage_type'] == found_this[0]:
            list1.append(elements['ship_name'])
    return ', '.join(list1)

################################################################
####                      Bot commands                      ####
################################################################

# quick countodwn hack until Phoenix II Birthday on 2019 June 28
@bot.command()
async def bday(ctx):
    if ctx.invoked_subcommand is None:
        present = datetime.datetime.now()
        future = datetime.datetime(2019, 7, 28, 8, 0, 0)
        difference = future - present
        await ctx.send(difference)

@bot.command()
async def source(ctx):
    src = "https://github.com/Phoenix-II-Community/apex-bot"
    await ctx.send(src)


@bot.group()
async def ship(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid ship command passed.')

@ship.command()
async def weapon(ctx, *, arg1):
    list_of_ships = wpn_dmg_search(arg1)
    await ctx.send(list_of_ships)

@ship.command()
async def aura(ctx, *, arg1):
    list_of_ships = aura_search(arg1)
    await ctx.send(list_of_ships)

@ship.command()
async def zen(ctx, *, arg1):
    list_of_ships = zen_search(arg1)
    await ctx.send(list_of_ships)

# Sub command to the @bot.group() decorator ship function.
# Intended that for use in high traffic channels, the output size is intential 
# small. A 5 line embed with basic info: name, weapon, dps, aura and zen.
@ship.command()
async def info(ctx, *, arg1):
    ship_name = ship_search(arg1)
    ship_embed_title = get_ship_title(ship_name)
    ship_embed_description = get_ship_description_small(ship_name)
    embed_colour = get_em_colour(ship_name)
    embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
    embed.set_thumbnail(url=get_ship_image(ship_name))
    await ctx.send(embed=embed)

@ship.command()
async def number(ctx, *, arg1):
    ship_name = ship_search(arg1)
    number = find_number(ship_name)
    await ctx.send(number)

# Sub command to the @bot.group() decorator ship function.
# Intended that for use in low traffic channels, the output size is large.
# A 6+ line embed with detailed info: name, weapon, dps, aura and zen.
@ship.command()
async def detail(ctx, *, arg1):
    ship_name = ship_search(arg1)
    ship_embed_title = get_ship_title(ship_name)
    ship_embed_description = get_ship_description_small(ship_name)
    embed_colour = get_em_colour(ship_name)
    embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
    embed.set_thumbnail(url=get_ship_image(ship_name))
    await ctx.send(embed=embed)


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
