#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
import settings
import os 
import sys, traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = ['!']
    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.simple',
                      'cogs.invader',
                      'cogs.daily',
                      'cogs.apex',
                      'cogs.img',
                      'cogs.ship'
                      ]

bot = commands.Bot(
    command_prefix=get_prefix, 
    description='Phoenix 2 iOS information bot',
    # my current ID, change to yours when running
    owner_id=330274890802266112)


# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()
            
@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print('We have logged in as {0.user}'.format(bot))

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    game = discord.Game("Testing Cogs")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'Successfully logged in and booted...!')

################################################################
####                      Bot commands                      ####
################################################################

# If a message receives the :el: emoji, then the bot should add it's own :el: reaction
@bot.event
async def on_reaction_add(reaction, user):
    # we do not want the bot to react to its own reaction
    if user == bot.user:
        return
    elif str(reaction.emoji) == "<:el:373097097727049728>":
        emoji = get(bot.emojis, name='el')
        await reaction.message.add_reaction(emoji)
        return
    elif str(reaction.emoji) == "<:ogonisfine:583241232768303105>":
        emoji = get(bot.emojis, name='ogonisfine')
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
    elif 'ogon is fine' in message.content:
        emoji = get(bot.emojis, name='ogonisfine')
        await message.add_reaction(emoji)
        return
bot.run(settings.discordkey)