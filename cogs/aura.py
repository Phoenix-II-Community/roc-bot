#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands
from res.data import ShipData, CategoryLister, ShipLister


#### Aura
# ```
# /aura                       list of Auras
# /aura <aura>                list of ships with an aura (supports shortcuts)
# /aura detail <aura>         detailed aura info
# /aura help
# ```
class AuraCog(commands.Cog, group_name="aura"):
    """AuraCog"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Aura cog loaded...')

    @commands.hybrid_group(name="aura")
    @commands.guild_only()
    async def aura(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid aura command passed.')


    @aura.command(name='all', description='list of all the Auras', help='list of all the Auras')
    @commands.guild_only()
    async def all(self, ctx):
        sc = 'aura'
        await ctx.send(embed=CategoryLister(self, sc).embed_list)

    @aura.command(name='list', help='list of ships with the aura')
    @commands.guild_only()
    async def list(self, ctx, *, aura_name=None):
        sc = 'aura'
        await ShipLister(self, ctx, aura_name, sc).create_embed()


    @aura.command(name='info', help=' info about an aura')
    @commands.guild_only()
    async def info(self, ctx, *, aura_type=None):
        if aura_type is None:
            await ctx.send("coming soon")
        else:
            await ctx.send("coming soon")        #await ctx.send(embed=CategoryLister(self, sc, aura_type).embed_list)


# The setup fucntion below is neccesarry. Remember we give client.add_cog() the
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(AuraCog(client))
