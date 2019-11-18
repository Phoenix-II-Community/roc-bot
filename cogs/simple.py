#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import client


class SimpleCog(commands.Cog, name="Simple Commands"):
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repeat', aliases=['copy', 'mimic'])
    @commands.guild_only()
    async def do_repeat(self, ctx, *, our_input: str):
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""

        await ctx.send(our_input)

    @commands.command(name='ping')
    @commands.guild_only()
    async def ping(self, ctx):
        await ctx.send(f"pong! {round(client.latency * 1000)}ms")

    @commands.command(name='source')
    @commands.guild_only()
    async def source(self, ctx):
        src = "https://github.com/Phoenix-II-Community/apex-bot"
        await ctx.send(src)

    @commands.command(name='me')
    @commands.is_owner()
    async def only_me(self, ctx):
        """A simple command which only responds to the owner of the bot."""

        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!!')

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(SimpleCog(bot))
