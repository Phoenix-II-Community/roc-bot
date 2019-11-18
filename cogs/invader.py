#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from invader_func import invader_type_list, invader_embed

class InvaderCog(commands.Cog, name="Invader Commands"):
    """InvaderCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['invaders'])
    @commands.guild_only()
    async def invader(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid invader command passed.')

    @invader.command()
    async def name(self, ctx, *, arg1=None):
        invader_embed_title = "Invader stats"
        invader_embed_description = invader_type_list(arg1)
        embed = discord.Embed(title=invader_embed_title, description=invader_embed_description)
        await ctx.send(embed=embed)


    @invader.command()
    async def turrets(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=invader_embed(sub_command))

    @invader.command()
    async def unprotected(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=invader_embed(sub_command))

    @invader.command()
    async def armored(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=invader_embed(sub_command))

    @invader.command()
    async def shielded(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=invader_embed(sub_command))

    @invader.command()
    async def invsplit(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=invader_embed(sub_command))

def setup(bot):
    bot.add_cog(InvaderCog(bot))
