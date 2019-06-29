#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import settings
import discord
import argparse
import shlex
from shlex import split

from discord.ext import commands
import json

# Open the required json files and assign it to a variable foo_data
ships_json = open('/Users/peter.carstairs/scripts/apex-bot/res/ships.json')
ships_data = json.load(ships_json)
invaders_json = open('/Users/peter.carstairs/scripts/apex-bot/res/invaders.json')
invaders_data = json.load(invaders_json)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

# Ship.json stat gathering function
def ship_stat(ship_name, stat_name):
    for element in ships_data[ship_name]:
        stat_value = element[stat_name]
        return stat_value

# Variable embeded colour function
def em_colour(type):
    if type == "sb":
        return 0x3a77f9
    elif type == "hi":
        return 0xee4529
    elif type == "ap":
        return 0xffb820


# Variable damage_type emoji function
def em_emojidmg(type):
    emojisb = "<:sb:572354637336936448>"
    emojihi = "<:hi:572354637043335169>"
    emojiap = "<:ap:572354637320159252>"
    if type == "sb":
        return emojisb
    elif type == "hi":
        return emojihi
    elif type == "ap":
        return emojiap

# Variable rarity emoji function
def em_emojirarity(type):
    emojicommon = "<:common:576427314368217128>"
    emojirare = "<:rare:576427437831880714>"
    emojisuperrare = "<:superrare:576427437844332544>"
    if type == "common":
        return emojicommon
    elif type == "rare":
        return emojirare
    elif type == "superrare":
        return emojisuperrare

invader_help = '''
**HELP**
`!invader -h` invader help
`!invader -l` invader names and turret count
`!invader -n <invader_name>` named invader HP stats for all affinities
`!invader -a <affinity>` all invaders HP that match the affinity
'''

class Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)


client = MyClient()
bot = commands.Bot(command_prefix="'")

# Bot function for ship calls
# This requires some changes to enable arg passing of 1 or 2 arguments as well as error handling.
# @bot.command()
# async def ship(ctx, arg1):
#     ship_embed_title = em_emojirarity(ship_stat(arg1, "rarity")) + " " + ship_stat(arg1, "ship_name")
#     ship_embed_description = em_emojidmg(ship_stat(arg1, "damage_type")) + " " + str(ship_stat(arg1, "damage_output"))
#     ship_embed_zen = ship_stat(arg1, "zen")
#     ship_embed_aura = ship_stat(arg1, "aura")
#     embed_colour = em_colour(ship_stat(arg1, "damage_type"))
#     embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
#     embed.add_field(name="Aura", value=ship_embed_aura, inline=False)
#     embed.add_field(name="Zen", value=ship_embed_zen, inline=False)
#     await ctx.send(embed=embed)
#     return

@bot.command()
async def invader(ctx, *, args):
    # start the arg parser using the vanilla argparse class
    ship_parser = Arguments(prog='bot')
    # add a argument for input from the CLI or in this case from a discord message
    ship_parser.add_argument('ship')
    #try:
    #    args_var = ship_parser.parse_args(shlex.split(ship))
    #    ship_input = args_var.ship
    #    send_ship_data = ship_stat(ship_input, "zen")
    #except RuntimeError as e:
    #    return await ctx.send(e)
    a = shlex.split(args)
    await ctx.send(a)
    return

@bot.group()
async def ship(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid ship command passed...')

@ship.command()
async def info(ctx, arg1):
      ship_embed_title = em_emojirarity(ship_stat(arg1, "rarity")) + " " + ship_stat(arg1, "ship_name")
      ship_embed_description = em_emojidmg(ship_stat(arg1, "damage_type")) + " " + str(ship_stat(arg1, "damage_output"))
      ship_embed_zen = ship_stat(arg1, "zen")
      ship_embed_aura = ship_stat(arg1, "aura")
      embed_colour = em_colour(ship_stat(arg1, "damage_type"))
      embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
      embed.add_field(name="Aura", value=ship_embed_aura, inline=False)
      embed.add_field(name="Zen", value=ship_embed_zen, inline=False)
      await ctx.send(embed=embed)
      return

bot.run(settings.discordkey)
