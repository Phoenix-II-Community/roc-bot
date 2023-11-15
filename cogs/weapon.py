#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands
from res.data import ShipData, CategoryLister, ShipLister

# Previously this was under the ship cog and it's a straight copy/paste.
# There's nothing in game that referred to affinity so that's being renamed and
# put under this weapon cog meaning bot commands align with the in game words better.
class WeaponCog(commands.Cog, group_name="weapon"):
    """WeaponCog"""

    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Weapon cog loaded...')

    @commands.hybrid_group(name="weapon", alias='wpn')
    @commands.guild_only()
    async def weapon(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid weapon command passed.')

    # list the weapon damage types (sb/hi/ap) and their characteristics
    @weapon.command(name='affinity',
                    help='List the weapon damage types and their characteristics')
    @commands.guild_only()
    async def affinity(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=CategoryLister(self, sc).embed_list)

    @weapon.command(name='damage',
                    help='list of Damage brackets or list of ships if value is given')
    @commands.guild_only()
    async def damage(self, ctx, *, damage_amount=None):
        sc = 'dmg'
        if damage_amount is None:
            await ctx.send(embed=CategoryLister(self, sc).embed_list)
        else:
            await ShipLister(self, ctx, damage_amount, sc).create_embed()


    @weapon.command(name='highimpact',
                    help='List ships with High Impact affinity type',
                    aliases=['hi'])
    @commands.guild_only()
    async def damage(self, ctx, *, arg1='hi'):
        sc = 'affinity'
        arg1 = 'hi'
        await ShipLister(self, ctx, arg1, sc).create_embed()

    @weapon.command(name='armorpiercing',
                    help='List ships with Armor Piercing affinity type',
                    aliases=['ap'])
    @commands.guild_only()
    async def damage(self, ctx):
        sc = 'affinity'
        arg1 = 'ap'
        await ShipLister(self, ctx, arg1, sc).create_embed()

    @weapon.command(name='shieldbreaker',
                    help='List ships with Shield Breaker affinity type',
                    aliases=['sb'])
    @commands.guild_only()
    async def damage(self, ctx):
        sc = 'affinity'
        arg1 = 'sb'
        await ShipLister(self, ctx, arg1, sc).create_embed()

# The setup fucntion below is neccesarry. Remember we give client.add_cog() the
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(WeaponCog(client))
