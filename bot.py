#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
import settings
from typing import Optional, Literal
import sys, traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def get_prefix(client, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = ['!']
    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(client, message)

initial_extensions = ['cogs.simple',
        'cogs.aura',
        'cogs.ship',
        #'cogs.invader',
        'cogs.daily',
        'cogs.img',
        'cogs.zen',
        'cogs.weapon'
        ]
# Here we load our extensions (cogs) listed above in [initial_extensions].
async def load():
    for extension in initial_extensions:
        try:
            await client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

client = commands.Bot(
        command_prefix=get_prefix,
        description='Phoenix 2 iOS information bot',
        # my current ID, change to yours when running
        owner_id=330274890802266112,
        intents=intents
        )


# Here we load our extensions (cogs) listed above in [initial_extensions].
async def load():
    for extension in initial_extensions:
        try:
            await client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

class RocBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all(),
        #NinjaPanda ID, change to yours while running.
        description='Pheonix 2 iOS information bot', owner_ids= [330274890802266112])

    async def setup_hook(self) -> None:
        await load()

client = RocBot()


# Here we load our extensions(cogs) listed above in [initial_extensions].
async def main():
    async with client:
        #await client.load_extension('cogs.ship')
        await client.start(settings.discordkey)

# if __name__ == '__main__':
#     for extension in initial_extensions:
#         try:
#             client.load_extension(extension)
#         except Exception as e:
#             print(f'Failed to load extension {extension}.', file=sys.stderr)
#             traceback.print_exc()

@client.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'We have logged in as {client.user}')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    game = discord.Game("Flying Centurion")
    await client.change_presence(status=discord.Status.online, activity=game)
    print(f'Successfully logged in and booted...!')

################################################################
####                      Bot commands                      ####
################################################################

# If a message receives the :el: emoji, then the bot should add it's own :el: reaction
@client.event
async def on_reaction_add(reaction, user):
    # we do not want the bot to react to its own reaction
    if user == client.user:
        return
    elif str(reaction.emoji) == "<:el:373097097727049728>":
        emoji = get(client.emojis, name='el')
        await reaction.message.add_reaction(emoji)
        return
    elif str(reaction.emoji) == "<:ogonisfine:583241232768303105>":
        emoji = get(client.emojis, name='ogonisfine')
        await reaction.message.add_reaction(emoji)
        return

# If someone uses the :el: emoji in a message then the bot should add it's own :el: reaction to the message.
@client.event
async def on_message(message):
    await client.process_commands(message)
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if ':el:' in message.content:
        emoji = get(client.emojis, name='el')
        await message.add_reaction(emoji)
    elif 'ogon is fine' in message.content:
        emoji = get(client.emojis, name='ogonisfine')
        await message.add_reaction(emoji)
        return


@client.hybrid_command()
async def test(ctx):
    await ctx.send("This is a hybrid command!")


@client.command(name='sync')
@commands.guild_only()
@commands.is_owner()
#!sync -> Syncs to global
#!sync ~ -> Syncs to guild only
#!sync * -> Copies all to guild and syncs to global
#!sync ^ -> Removes all from guild and re-syncs to guild.
async def sync(ctx: commands.Context,
               guilds: commands.Greedy[discord.Object],
               spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()
        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1
    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


asyncio.run(main())
#client.run(settings.discordkey)
