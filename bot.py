#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
import settings
from ship import generic_ship_command_embed, damagelisting, auralisting, zenlisting, raritylisting, affinitylisting, affinity_search, bot, random_ship_command_embed, all_ship_command_embed, ship_search, info_embed, find_number, detail_embed
import os 
from pathlib import Path
import json

# Open the required json files and assign it to a variable foo_data
cwd = os.getcwd()
invaders_json = open(f'{cwd}/res/invaders.json')
invaders_data = json.load(invaders_json)

logging.basicConfig(level=logging.INFO)

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

def get_invader_list(sub_command):
    invader_dict = invaders_data[sub_command]
    list1 = []
    for k, v in invader_dict.items():
        list1.append(("{key} {value}").format(key=k, value=v))
    return '\n'.join(list1)

def invader_embed(sub_command):
    ship_embed_title = "Hacky title fix me"
    ship_embed_description = get_invader_list(sub_command)
    embed = discord.Embed(  title=ship_embed_title, 
                            description=ship_embed_description)
    return embed

@bot.group(aliases=['invaders'])
async def invader(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid invader command passed.')

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
async def hullshield(ctx, *, arg1=None):
    sub_command = ctx.subcommand_passed
    await ctx.send(embed=invader_embed(sub_command))

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