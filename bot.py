#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import settings
import discord
import functools
import inspect
import typing

from discord.ext import commands
import json
from discord.utils import get
from functools import partial

# Create variable json_data assign the opening of a file to it
ships_json = open('/Users/peter.carstairs/scripts/apex-bot/res/ships.json')
print(ships_json)
ships_data = json.load(ships_json)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

def ship_stat(ship_name, stat_name):  # <-- note, you don't have to call it arg1 in the other functions, they can
    # make up their own name for it that will only be used within that function,
    # so the code is more descriptive returns the first seen stat for the given
    # ship name and stat name
    for element in ships_data[ship_name]:
        stat_value = element[stat_name]
        return stat_value


def em_colour(type):
    if type == "sb":
        return 0x3a77f9
    elif type == "hi":
        return 0xee4529
    elif type == "ap":
        return 0xffb820


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

client = MyClient()
bot = commands.Bot(command_prefix='!')


def customemoji(search):
    iconemoji = discord.utils.get(emojis(), name=search)
    return iconemoji

@bot.command()
async def ships(ctx, arg1):
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


#@bot.command()
#async def invaders(ctx, arg1):
#    for element in jdata[arg1]:
#        await ctx.send(element['ship_name'] + "\n" + \
#                       element['damage type'] + "\n" + \
#                       str(element['damage output']) + "\n" + \
#                       element['weapon_name'] + "\n" + \
#                       element['aura'] + "\n" + \
#                       element['zen'] + "\n" + \
#                       ":" + element['r'] + ":")
#        return


bot.run(settings.discordkey)
