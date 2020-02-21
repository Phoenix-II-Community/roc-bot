#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from invader_class import invader_type

class InvaderCog(commands.Cog, name="Invader Commands"):
    """InvaderCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['invaders'])
    @commands.guild_only()
    async def invader(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if ctx.invoked_subcommand is None and arg1 is None:
            await ctx.send('Invalid invader command passed.')
        else:
            await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def turrets(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def unprotected(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def armored(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def shielded(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def split(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

def setup(bot):
    bot.add_cog(InvaderCog(bot))
