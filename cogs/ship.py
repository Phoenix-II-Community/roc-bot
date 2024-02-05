#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands
from res.data import ShipData, CategoryLister, ShipLister


class ShipCog(commands.Cog, group_name="ship"):
    """ShipCog"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ship cog loaded...')

    @commands.hybrid_group(name="ship")
    @commands.guild_only()
    async def ship(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid ship command passed.')

    # Sub command to the @client.group() decorator ship function.
    # Intended that for use in high traffic channels, the output size is 
    # intentialy small. 
    # A 5 line embed with basic info: name, weapon, dps, aura and zen.
    @ship.command(name='info')
    @commands.guild_only()
    async def info(self, ctx, *, ship_name: str):
        await ctx.send(embed=ShipData(self, ship_name).embed_info)

    # Sub command to the @client.group() decorator ship function.
    # Intended that for use in low traffic channels, the output size is large.
    # A 6+ line embed with detailed info: name, weapon, dps, aura and zen.
    @ship.command(name='detail')
    @commands.guild_only()
    async def detail(self, ctx, *, ship_name: str):
        print(ctx.channel.id)
        if ctx.channel.id in [378546862627749908, 596343881705062417, 1166027391089512499]:
            await ctx.send(embed=ShipData(self, ship_name).embed_detail)
        else:
            await ctx.send("Command limited to <#378546862627749908>.")

    # @ship.command(name='zen')
    # @commands.guild_only()
    # async def zen(self, ctx, *, arg1=None):
    #     sc = ctx.command.name
    #     if arg1 is None:
    #         await ctx.send(embed=CategoryLister(self, sc).embed_list)
    #     else:
    #         await ShipLister(self, ctx, arg1, sc).create_embed()

    @ship.command(name='rarity',help='lists the rarities or the ships of that rarity')
    @commands.guild_only()
    async def rarity(self, ctx, *, rarity_name=None):
        sc = ctx.command.name
        if ctx.channel.id in (378546862627749908, 596343881705062417, 1166027391089512499):
            if rarity_name is None:
                await ctx.send(embed=CategoryLister(self, sc).embed_list)
            else:
                await ShipLister(self, ctx, rarity_name, sc).create_embed                                                                                                                                                                                                                                                                                                                                          ()
        else:
            await ctx.send("Command limited to <#378546862627749908>.")

    @ship.command(name='random')
    @commands.guild_only()
    async def rand(self, ctx, *, qty=None):
        sc = ctx.command.name
        if ctx.channel.id in (378546862627749908, 596343881705062417, 1166027391089512499):
            if qty is None:
                arg1 = 10
            await ShipLister(self, ctx, qty, sc).create_embed()
        else:
            await ctx.send("Command limited to <#378546862627749908>.")

    @ship.command(name='all',
                  help='list all 100 ships')
    @commands.guild_only()
    async def all(self, ctx, *, arg1=None):
        sc = ctx.command.name
        arg1 = None
        if ctx.channel.id in (378546862627749908, 596343881705062417, 1166027391089512499):
            await ShipLister(self, ctx, arg1, sc).create_embed()
        else:
            await ctx.send("Command limited to <#378546862627749908>.")


# The setup fucntion below is neccesarry. Remember we give client.add_cog() the 
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(ShipCog(client))
