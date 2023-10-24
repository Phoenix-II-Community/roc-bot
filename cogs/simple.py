#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands
from discord import client


class SimpleCog(commands.Cog, name="Simple Commands"):
    """SimpleCog"""
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Simple loaded...')

    @commands.command(name='repeat', description='Sends what you type', with_app_command=True)
    @commands.guild_only()
    async def do_repeat(self, ctx: commands.Context, your_input: str) -> None:
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""
        await ctx.send(your_input)

    #@commands.command(name='ping')
    #@commands.guild_only()
    #async def ping(self, ctx):
    #    await ctx.send(f"pong! {round(self.bot.discord.client.latency * 1000)}ms")

    @commands.command(name='source', description='GitHub repository link')
    @commands.guild_only()
    async def source(self, ctx):
        src = "https://github.com/Phoenix-II-Community/apex-bot"
        await ctx.send(src)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(SimpleCog(client))
