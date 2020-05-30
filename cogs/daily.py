#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from res.mission import Mission


class DailyCog(commands.Cog, name="Daily Commands"):
    """InvaderCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['mission'])
    @commands.guild_only()
    async def daily(self, ctx):
        if ctx.invoked_subcommand is None:
            sub_command = ctx.subcommand_passed
            await ctx.send(embed=Mission(self, sub_command).embed_daily)

    @daily.command()
    async def next(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=Mission(self, sub_command).embed_daily)

def setup(bot):
    bot.add_cog(DailyCog(bot))
