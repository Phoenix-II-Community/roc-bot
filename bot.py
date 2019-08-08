#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import discord.ext.commands
import re
import unicodedata

home_dir = Path.home()

# Open the required json files and assign it to a variable foo_data
ships_json = open(('{hd}/scripts/apex-bot/res/ships.json').format(hd=home_dir))
ships_data = json.load(ships_json)
invaders_json = open(('{hd}/scripts/apex-bot/res/invaders.json').format(hd=home_dir))
invaders_data = json.load(invaders_json)

embed_colours = {"Shield Breaker": 0x3a77f9, "High Impact": 0xee4529, "Armor Piercing": 0xffb820}

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
# This function uses one of the 3 affinity choices to select a colour from
# the embed_colours variable (red/yellow/blue)
def get_em_colour(ship_name):
    ship_dict = ships_data[ship_name]
    dmg_type = ship_dict["affinity"]
    em_colour = embed_colours[dmg_type]
    return em_colour

# This is the small embed description output used by the
#  "!ship info <ship name>" command. 
def get_ship_description_small(ship_name):
    ship_dict = ships_data[ship_name]
    ship_description_small = ("{emojidps} {ship[dmg]}\n"
    "{emojidmgtype} {ship[weapon_name]}\n"
    "{emojiaura} {ship[aura]}\n"
    "{emojizen} {ship[zen]}\n").format(emojidps=customemoji("dps"),
            emojidmgtype=customemoji(ship_dict["affinity"]),
            emojiaura=customemoji(ship_dict["aura"]),
            emojizen=customemoji(ship_dict["zen"]),
            ship=ship_dict)
    return ship_description_small

# Each ship has a number based on the in game order they were listed and added.
# return that100% number. 
def find_number(ship_name):
    ship_dict = ships_data[ship_name]
    number = ship_dict["number"]
    return number

# Creates the title of the discord emebed consisting of the rarity emoji 
# the ship name.
def get_ship_title(ship_name):
    ship_dict = ships_data[ship_name]
    ship_title = ("{rarityemoji} {nameofship}").format(\
        rarityemoji=customemoji(ship_dict["rarity"]), 
        nameofship=ship_dict["ship_name"])
    return ship_title

def get_ship_image(ship_name):
    urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/img/"
    url = ("{giturl}{shipname}.png").format(giturl=urlgit, shipname=ship_name)
    return url



# Making a set of elements found based on the sub command string that's used.
# The sub command string matches a ship.json key.  
def make_element_set(ctxsc):
    new_set = set({})
    for elements in ships_data.values():
        new_set.add(elements[ctxsc])
    return sorted(new_set)

# A standard list used by many funcitons to output a list 
# affinity emoji, ship emoji, ship name. 
def generic_ship_list(found_this, ctxsc):
    list1 = []
    for elements in ships_data.values():
        if elements[ctxsc] == found_this[0]:
            list1.append(("{elementemoji} {shipemoji} {name}").format(\
                elementemoji=customemoji(elements['affinity']), \
                shipemoji=customemoji(elements['ship_name'].lower()),\
                name=elements['ship_name']))
    return '\n'.join(list1)

def ship_command_title(found_this, ctxsc):
    if ctxsc == "dmg":
        var_title = ("{dpsemoji} DPS {dps}").format(dpsemoji=customemoji("dps"), \
            dps=found_this[0])
    else:
        var_title = ("{emoji} {rarity} Ships").format(emoji=customemoji(found_this[0]), \
            rarity=found_this[0])
    return var_title

def ship_command_common_query(find_this, ctxsc):
    found_this = process.extractOne(find_this, make_element_set(ctxsc))
    description = generic_ship_list(found_this, ctxsc)
    title = ship_command_title(found_this, ctxsc)
    embed = discord.Embed(title=title, description=description)
    return embed

  
def affinity_search(find_this, ctxsc):
    list1 = []
    if find_this == "ap":
        find_this = "Armor Piercing"
    elif find_this == "hi":
        find_this = "High Impact"
    elif find_this == "sb":
        find_this = "Shield Breaker"
    else:
        pass
    found_this = process.extractOne(find_this, make_element_set(ctxsc))
    for elements in ships_data.values():
        if elements['affinity'] == found_this[0]:
            list1.append(("{emoji} {name}").format(emoji=customemoji(elements['ship_name'].lower()),
             name=elements['ship_name']))
        description = '\n'.join(list1)
        title = ("{emoji} {affinity} Ships").format(emoji=customemoji(found_this[0]), \
            affinity=found_this[0])
        em_colour = embed_colours[found_this[0]]
        embed = discord.Embed(title=title, description=description, colour=em_colour)
    return embed

def sanitise_input(input_string):
    words_only = re.sub('\W+','', input_string)
    return unicodedata.normalize('NFKD', words_only).encode('ascii', 'ignore').decode('utf8')

def customemoji(find_this):
    find_sanitised = sanitise_input(find_this.lower())
    return discord.utils.get(bot.emojis, name = find_sanitised)

def auralisting(ctxsc):
    list1 = []
    for elements in make_element_set(ctxsc):
        list1.append(("{emoji} {name}").format(
            emoji=customemoji(elements),
            name=elements))
    description = '\n'.join(list1)
    title = ("Auras")
    return discord.Embed(title=title, description=description)

def zenlisting(ctxsc):
    list1 = []
    for elements in make_element_set(ctxsc):
        list1.append(("{emoji} {name}").format(
            emoji=customemoji(elements),
            name=elements))
    description = '\n'.join(list1)
    title = ("Zens")
    return discord.Embed(title=title, description=description)

def affinitylisting(ctxsc):
    list1 = []
    for elements in make_element_set(ctxsc):
        list1.append(("{emoji} {name}").format(
            emoji=customemoji(elements),
            name=elements))
    description = '\n'.join(list1)
    title = ("Main Weapon Affinities")
    return discord.Embed(title=title, description=description)

def damagelisting(ctxsc):
    list1 = []
    for elements in make_element_set(ctxsc):
        list1.append(("{name}").format(name=elements))
    description = '\n'.join(list1)
    title = ("{dpsemoji} Damage Brackets").format(dpsemoji=customemoji("dps"))
    return discord.Embed(title=title, description=description)

def raritylisting(ctxsc):
    list1 = []
    for elements in make_element_set(ctxsc):
        list1.append(("{emoji} {name}").format(
            emoji=customemoji(elements),
            name=elements))
    description = '\n'.join(list1)
    title = ("{rareemoji} Rarities").format(rareemoji=customemoji("vegemite"))
    return discord.Embed(title=title, description=description)


#def zenlisting():


################################################################
####                      Bot commands                      ####
################################################################

# quick countodwn hack until Phoenix II Birthday on 2019 June 28
@bot.command()
async def bday(ctx):
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
async def dmg(ctx, *, arg1=None):
    ctxsc = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=damagelisting(ctxsc))
    else:
        await ctx.send(embed=ship_command_common_query(arg1, ctxsc))


@ship.command()
async def aura(ctx, *, arg1=None):
    ctxsc = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=auralisting(ctxsc))
    else:
        await ctx.send(embed=ship_command_common_query(arg1, ctxsc))


@ship.command()
async def zen(ctx, *, arg1=None):
    ctxsc = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=zenlisting(ctxsc))
    else:
        await ctx.send(embed=ship_command_common_query(arg1, ctxsc))

@ship.command()
async def rarity(ctx, *, arg1=None):
    ctxsc = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=raritylisting(ctxsc))
    else:
        await ctx.send(embed=ship_command_common_query(arg1, ctxsc))


@ship.command()
async def affinity(ctx, *, arg1=None):
    ctxsc = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=affinitylisting(ctxsc))
    else:
        await ctx.send(embed=affinity_search(arg1, ctxsc))


# Sub command to the @bot.group() decorator ship function.
# Intended that for use in high traffic channels, the output size is intential 
# small. A 5 line embed with basic info: name, weapon, dps, aura and zen.
@ship.command()
async def info(ctx, *, arg1):
    ship_name = ship_search(arg1)
    ship_embed_title = get_ship_title(ship_name)
    ship_embed_description = get_ship_description_small(ship_name)
    embed_colour = get_em_colour(ship_name)
    embed = discord.Embed(title=ship_embed_title, 
    description=ship_embed_description, colour=embed_colour)
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
#@ship.command()
#async def detail(ctx, *, arg1):
#    ship_name = ship_search(arg1)
#    ship_embed_title = get_ship_title(ship_name)
#    ship_embed_description = get_ship_description_small(ship_name)
#    embed_colour = get_em_colour(ship_name)
#    embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
#    embed.set_thumbnail(url=get_ship_image(ship_name))
#    await ctx.send(embed=embed)


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