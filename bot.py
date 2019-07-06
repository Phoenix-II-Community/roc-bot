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


logging.basicConfig(level=logging.INFO)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

# ship.json stat gathering function
def ship_stat(ship_name, stat_name):
    for element in ships_data[ship_name]:
        stat_value = element[stat_name]
        return stat_value

# emoji.json stat gathering function
def emoji_stat(feature_name):
    for element in emoji_data[feature_name]:
        stat_value = element[feature_name]
        return stat_value

# Variable embeded colour function
def em_colour(type):
    if type == "sb":
        return 0x3a77f9
    elif type == "hi":
        return 0xee4529
    elif type == "ap":
        return 0xffb820

def emoji(key):
    emoji = emoji_data[key]
    return emoji

client = MyClient()
bot = commands.Bot(command_prefix="!")

@bot.group()
async def ship(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid ship command passed.')

@ship.command()
async def info(ctx, *, arg1):
      ship_embed_title = em_emojirarity(ship_stat(arg1, "rarity")) + " " + ship_stat(arg1, "ship_name")

      ship_embed_description = "<:dps:596613103941058560> " + str(ship_stat(arg1, "damage_output")) + "\n" \
                    + em_emojidmg(ship_stat(arg1, "damage_type")) + " " + (ship_stat(arg1, "weapon_name")) + "\n" \
                    + emoji(ship_stat(arg1, "aura")) + " " + ship_stat(arg1, "aura") + "\n" \
                    + emoji(ship_stat(arg1, "zen")) + " " + ship_stat(arg1, "zen")
      embed_colour = em_colour(ship_stat(arg1, "damage_type"))
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