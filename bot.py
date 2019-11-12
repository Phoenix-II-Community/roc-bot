#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
import settings
from ship import generic_ship_command_embed, damagelisting, auralisting, zenlisting, raritylisting, affinitylisting, affinity_search, bot, random_ship_command_embed, all_ship_command_embed, ship_search, info_embed, find_number, detail_embed, customemoji, sanitise_input
import os 
from pathlib import Path
import json
from fuzzywuzzy import process, fuzz
import re

# Open the required json files and assign it to a variable foo_data
cwd = os.getcwd()
invaders_json = open(f'{cwd}/res/invaders.json')
invaders_data = json.load(invaders_json)
imgsrch_json = open(f'{cwd}/res/imgsrch.json')
imgsrch_data = json.load(imgsrch_json)
ships_json = open(f'{cwd}/res/ships.json')
ships_data = json.load(ships_json)


logging.basicConfig(level=logging.INFO)

invaders = {"sparrow", "raven", "heron", "eagle", "vulture", "condor", "roc"}

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("Phoenix II")
    await bot.change_presence(status=discord.Status.online, activity=game)

################################################################
####                      Bot commands                      ####
################################################################

@bot.command()
async def source(ctx):
    src = "https://github.com/Phoenix-II-Community/apex-bot"
    await ctx.send(src)


@bot.group(aliases=['ships'])
async def ship(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid ship command passed.')


@ship.command()
async def dmg(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=damagelisting(sub_command))
    else:
        await generic_ship_command_embed(ctx, arg1, sub_command)

@ship.command()
async def aura(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=auralisting(sub_command))
    else:
        await generic_ship_command_embed(ctx, arg1, sub_command)


@ship.command()
async def zen(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=zenlisting(sub_command))
    else:
        await generic_ship_command_embed(ctx, arg1, sub_command)

@ship.command()
async def rarity(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    if ctx.channel.id == 378546862627749908:
        if arg1 == None:
            await ctx.send(embed=raritylisting(sub_command))
        else:
            await generic_ship_command_embed(ctx, arg1, sub_command)
    else:
        await ctx.send("Command limited to <#378546862627749908>.")


@ship.command()
async def affinity(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    if arg1 == None:
        await ctx.send(embed=affinitylisting(sub_command))
    else:
        await ctx.send(embed=affinity_search(arg1, sub_command))

@ship.command()
async def rand(ctx, *, arg1=None):
    if ctx.channel.id == 378546862627749908:
        if arg1 == None:
            arg1 = 10
            await random_ship_command_embed(ctx, arg1)
        else:
            await random_ship_command_embed(ctx, arg1)
    else:
        await ctx.send("Command limited to <#378546862627749908>.")

@ship.command()
async def all(ctx, *, arg1=None):
    if ctx.channel.id == 378546862627749908:
        await all_ship_command_embed(ctx)
    else:
        await ctx.send("Command limited to <#378546862627749908>.")

# Sub command to the @bot.group() decorator ship function.
# Intended that for use in high traffic channels, the output size is intential 
# small. A 5 line embed with basic info: name, weapon, dps, aura and zen.
@ship.command()
async def info(ctx, *, arg1):
    ship_name = ship_search(arg1)
    await ctx.send(embed=info_embed(ship_name))

@ship.command()
async def number(ctx, *, arg1):
    ship_name = ship_search(arg1)
    number = find_number(ship_name)
    await ctx.send(number)

#Sub command to the @bot.group() decorator ship function.
#Intended that for use in low traffic channels, the output size is large.
#A 6+ line embed with detailed info: name, weapon, dps, aura and zen.
@ship.command()
async def detail(ctx, *, arg1):
    if ctx.channel.id == 378546862627749908:
        ship_name = ship_search(arg1)
        await ctx.send(embed=detail_embed(ship_name))
    else:
        await ctx.send("Command limited to <#378546862627749908>.")

@bot.group()
async def shutdown(ctx):
    if ctx.author.id == 330274890802266112:    
        await ctx.send("Goodbye")
        await ctx.bot.logout()

def invader_title(sub_command):
    if sub_command == "invsplit":
        var_title = ("{invsplit} Shield and Unprotected HP Split").format(invsplit=customemoji("invsplit"))
    else:
        var_title = ("{emoji} {context} Invaders").format(emoji=customemoji(sub_command), \
            context=sub_command.capitalize())
    return var_title

def invder_search(find_this):
    found_this = process.extractOne(find_this, invaders)
    invader_name = found_this[0]
    return invader_name


def invader_type_list(arg1):
    list1 = []
    found_this = invder_search(arg1)
    for k, v in invaders_data.items():
        for kv in v.items():
            if kv[0] == found_this:
                    list1.append(("{invader} {stat}").format(invader=kv[0], stat=kv[1]))
    return '\n'.join(list1)




def get_invader_list(sub_command):
    invader_dict = invaders_data[sub_command]
    list1 = []
    for k, v in invader_dict.items():
        list1.append(("{key} {value}").format(key=k, value=v))
    return '\n'.join(list1)

def invader_embed(sub_command):
    invader_embed_title = invader_title(sub_command)
    invader_embed_description = get_invader_list(sub_command)
    embed = discord.Embed(  title=invader_embed_title, 
                            description=invader_embed_description)
    return embed


@bot.group(aliases=['invaders'])
async def invader(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid invader command passed.')

@invader.command()
async def name(ctx, *, arg1=None):
    invader_embed_title = "Invader stats"
    invader_embed_description = invader_type_list(arg1)
    embed = discord.Embed(title=invader_embed_title, description=invader_embed_description)
    await ctx.send(embed=embed)


@invader.command()
async def turrets(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    await ctx.send(embed=invader_embed(sub_command))

@invader.command()
async def unprotected(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    await ctx.send(embed=invader_embed(sub_command))

@invader.command()
async def armored(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    await ctx.send(embed=invader_embed(sub_command))

@invader.command()
async def shielded(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    await ctx.send(embed=invader_embed(sub_command))

@invader.command()
async def invsplit(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    await ctx.send(embed=invader_embed(sub_command))

def img_ship_search(find_this):
    print(type(find_this))
    found_this = process.extractOne(find_this, imgsrch_data, scorer=fuzz.token_sort_ratio)
    print(found_this)
    ship_name = found_this[0]
    return ship_name

def img_get_ship_title(ship_name):
    base_ship_name = re.sub( r"([A-Z])", r"", ship_name)
    ship_dict = ships_data[base_ship_name]
    ship_title = ("{rarityemoji} {nameofship}").format(\
        rarityemoji=customemoji(ship_dict["rarity"]), 
        nameofship=re.sub( r"([A-Z]+)", r" \1", ship_name))
    return ship_title

from ship import get_ship_title, get_em_colour, get_ship_image

@bot.group(aliases=['image'])
async def img(ctx, *, arg1):
    print(arg1)
    ship_name = img_ship_search(re.sub(r' ','', arg1))
    print(ship_name)
    base_ship_name = re.sub( r"([A-Z])", r"", ship_name)
    print(base_ship_name)
    ship_embed_title = img_get_ship_title(ship_name)
    embed_colour = get_em_colour(base_ship_name)
    embed = discord.Embed(title=ship_embed_title
    , colour=embed_colour)
    embed.set_image(url=get_ship_image(ship_name))
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

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if 'ogon is fine' in message.content:
        emoji = get(bot.emojis, name='ogonisfine')
        await message.add_reaction(emoji)
        return

bot.run(settings.discordkey)