#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import client


class ApexCog(commands.Cog, name="Apex Commands"):
    """ApexCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['apexs'])
    @commands.guild_only()
    async def apex(self, ctx):
        if ctx.invoked_subcommand is None:
            sub_command = ctx.subcommand_passed
            await ctx.send(embed=Mission(self, sub_command).embed_daily)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case ApexCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(ApexCog(bot))
