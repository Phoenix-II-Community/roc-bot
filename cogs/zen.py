#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands
from res.data import ShipData, CategoryLister, ShipLister


#### Zen
# ```
# /zen                       list of Zens
# /zen <zen>                list of ships with an zen (supports shortcuts)
# /zen detail <zen>         detailed zen info
# /zen find                 find ships with a zen
# /zen help
# ```
class ZenCog(commands.Cog, group_name="zen"):
    """ZenCog"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Zen cog loaded...')


    @commands.hybrid_group(name="zen")
    @commands.guild_only()
    async def zen(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid zen command passed.')

    @zen.command(name='all',description='All zens in the game',help='All zens in the game')
    @commands.guild_only()
    async def all(self, ctx):
        sc = 'zen'
        await ctx.send(embed=CategoryLister(self, sc).embed_list)

    @zen.command(name='list',help='All the ships with that Zen',description='All the ships with that Zen')
    @commands.guild_only()
    async def list(self, ctx, *, zen_name=None):
        sc = 'zen'
        await ShipLister(self, ctx, zen_name, sc).create_embed()


    @zen.command(name='info', help='List the zen damage types and their characteristics')
    @commands.guild_only()
    async def info(self, ctx, *, zen_type=None):
        if zen_type is None:
            await ctx.send("coming soon")
        else:
            await ctx.send("coming soon")
        #awiait ctx.send(embed=CategoryLister(self, sc, zen_type).embed_list)

# The setup function below is necessary. Remember we give client.add_cog() the
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(ZenCog(client))
