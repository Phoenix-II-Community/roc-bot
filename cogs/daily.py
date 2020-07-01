#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from mission import Mission


class DailyCog(commands.Cog, name="Daily Commands"):
    """InvaderCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['mission'], invoke_without_command = True)
    @commands.guild_only()
    async def daily(self, ctx, daily_number: int = None):
        if ctx.invoked_subcommand is None:
            sub_command = ctx.subcommand_passed
            await ctx.send(embed=Mission(self, sub_command, daily_number).embed_daily)
    
#    @commands.guild_only()
#    async def daily(self, ctx, daily_num: int):

#            await ctx.send(embed=Mission(self, sub_command, daily_num).embed_daily)

    @daily.command()
    async def next(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=Mission(self, sub_command).embed_daily)
    
    @daily.command()
    async def all(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=Mission(self, sub_command).embed_d_list)

def setup(bot):
    bot.add_cog(DailyCog(bot))
