#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands
from res.data import ShipData, CategoryLister, ShipLister

@app_commands.guild_only()
class ShipCog(commands.Cog, group_name="ship"):
    """ShipCog"""

    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ship cog loaded...')

    @commands.hybrid_group(aliases=['ships'])
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
    async def info(self, ctx, *, arg1: str):
        await ctx.send(embed=ShipData(self, arg1).embed_info)

    # Returns the ship in game sequence number. For example Shinova is number 1.
    @ship.command(name='number')
    @commands.guild_only()
    async def number(self, ctx, *, arg1: str):
        await ctx.send(ShipData(self, arg1).s_obj['number'])

    #Sub command to the @client.group() decorator ship function.
    #Intended that for use in low traffic channels, the output size is large.
    #A 6+ line embed with detailed info: name, weapon, dps, aura and zen.
    @ship.command(name='detail')
    @commands.guild_only()
    async def detail(self, ctx, *, arg1: str):
        print(ctx.channel.id)
        if ctx.channel.id in [378546862627749908,596343881705062417]:
            await ctx.send(embed=ShipData(self, arg1).embed_detail)
        else:
            await ctx.send("Command limited to <#378546862627749908>.")

    @ship.command(name='dmg')
    @commands.guild_only()
    async def dmg(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if arg1 is None:
            await ctx.send(embed=CategoryLister(self, sc).embed_list)
        else:
            await ShipLister(self, ctx, arg1, sc).create_embed()

    @ship.command(name='aura')
    @commands.guild_only()
    async def aura(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        print(f"######################## {ctx.subcommand_passed}")
        print(f"######################## {ctx.invoked_subcommand}")
        if arg1 is None:
            await ctx.send(embed=CategoryLister(self, sc).embed_list)
        else:
            await ShipLister(self, ctx, arg1, sc).create_embed()


    @ship.command(name='zen')
    @commands.guild_only()
    async def zen(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if arg1 is None:
            await ctx.send(embed=CategoryLister(self, sc).embed_list)
        else:
            await ShipLister(self, ctx, arg1, sc).create_embed()

    @ship.command(name='rarity')
    @commands.guild_only()
    async def rarity(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if ctx.channel.id == 378546862627749908:
            if arg1 is None:
                await ctx.send(embed=CategoryLister(self, sc).embed_list)
            else:
                await ShipLister(self, ctx, arg1, sc).create_embed()
        else:
            await ctx.send("Command limited to <#378546862627749908>.")


    @ship.command(name='affinity')
    @commands.guild_only()
    async def affinity(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if arg1 is None:
            await ctx.send(embed=CategoryLister(self, sc).embed_list)
        else:
            await ShipLister(self, ctx, arg1, sc).create_embed()

    @ship.command(name='rand')
    @commands.guild_only()
    async def rand(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if ctx.channel.id == 378546862627749908:
            if arg1 is None:
                arg1 = 10
            await ShipLister(self, ctx, arg1, sc).create_embed()
        else:
            await ctx.send("Command limited to <#378546862627749908>.")

    @ship.command(name='all')
    @commands.guild_only()
    async def all(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if ctx.channel.id in (378546862627749908,596343881705062417):
            await ShipLister(self, ctx, arg1, sc).create_embed()
        else:
            await ctx.send("Command limited to <#378546862627749908>.")


# The setup fucntion below is neccesarry. Remember we give client.add_cog() the 
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(ShipCog(client))
