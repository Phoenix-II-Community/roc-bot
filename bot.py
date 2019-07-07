#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import settings
import discord
import logging
from discord.utils import get
from discord.ext import commands
import json

# Open the required json files and assign it to a variable foo_data
ships_json = open('/Users/peter.carstairs/scripts/apex-bot/res/ships.json')
ships_data = json.load(ships_json)
invaders_json = open('/Users/peter.carstairs/scripts/apex-bot/res/invaders.json')
invaders_data = json.load(invaders_json)
emoji_json = open('/Users/peter.carstairs/scripts/apex-bot/res/emoji.json')
emoji_data = json.load(emoji_json)


embed_colours = {"sb": 0x3a77f9, "hi": 0xee4529, "ap": 0xffb820}

logging.basicConfig(level=logging.INFO)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

# ship.json stat gathering function
def ship_stat(ship_name, stat_name):
    for element in ships_data[ship_name.lower()]:
        stat_value = element[stat_name]
        return stat_value


# emoji.json stat gathering function
def emoji_stat(feature_name):
    for element in emoji_data[feature_name]:
        stat_value = element[feature_name]
        return stat_value

def get_em_colour(arg1):
    dmg_type = ship_stat(arg1, "damage_type")
    em_colour = embed_colours[dmg_type]
    return em_colour

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

# Creates the title of the discord emebed consisting of the rarity emoji and the ship name.
def get_ship_title(arg1):
    ship_title = emoji(ship_stat(arg1, "rarity")) + " " + ship_stat(arg1, "ship_name")
    return ship_title

# receives the element from ships.json maybe another file in future and uses it as a key in emoji.json.
def emoji(key):
    emoji = emoji_data[key]
    return emoji

client = MyClient()
bot = commands.Bot(command_prefix="!")

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
      await ctx.send(embed=embed)
      return

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
