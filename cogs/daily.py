#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from res.mission import Mission


class DailyCog(commands.Cog, name="Daily Commands"):
    """InvaderCog"""

    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Daily cog loaded...')

    @commands.hybrid_command(name='daily', description='guesses the current mission')
    @commands.guild_only()
    async def daily(self, ctx):
        if ctx.invoked_subcommand is None:
            sub_command = ctx.subcommand_passed
            await ctx.send(embed=Mission(self, sub_command).embed_daily)

    @commands.hybrid_command(name='next', description='guesses the next mission')
    async def next(self, ctx, *, arg1=None):
        sub_command = ctx.subcommand_passed
        await ctx.send(embed=Mission(self, sub_command).embed_daily)

async def setup(client) -> None:
    await client.add_cog(DailyCog(client))

