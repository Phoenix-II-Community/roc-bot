#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from invader_func import invader_type_list, invader_embed
from img_func import img_get_ship_title, img_ship_search, get_em_colour
from ship_func import get_ship_image
import re
class ImgageCog(commands.Cog, name="Imgage Commands"):
    """ImgageCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='img')
    @commands.guild_only()
    # arg1 is everthing after the command
    async def img(self, ctx, *, arg1):
        # The img_ship_search function compares against a JSON file 
        # the file has all ship names with base name in lowercase and apex in 
        # all uppercase. We're using fuzzywuzzy to find the best match but 
        # before finding it, we remove all white space from the string. 
        ship_name = img_ship_search(re.sub(r' ','', arg1))
        # For the formatting reasons we need the base ship name so we can search
        # against other JSON files. This strips all upper case letters which
        # will be the apex name. 
        base_ship_name = re.sub( r"([A-Z])", r"", ship_name)
        
        ship_embed_title = img_get_ship_title(self, ship_name)
        embed_colour = get_em_colour(base_ship_name)
        embed = discord.Embed(title=ship_embed_title
        , colour=embed_colour)
        embed.set_image(url=get_ship_image(ship_name))
        await ctx.send(embed=embed)


    @commands.command(name='img2')
    @commands.guild_only()
    # arg1 is everthing after the command
    async def img2(self, ctx, *, arg1):
        # The img_ship_search function compares against a JSON file 
        # the file has all ship names with base name in lowercase and apex in 
        # all uppercase. We're using fuzzywuzzy to find the best match but 
        # before finding it, we remove all white space from the string. 
        ship_name = img_ship_search(re.sub(r' ','', arg1))
        # For the formatting reasons we need the base ship name so we can search
        # against other JSON files. This strips all upper case letters which
        # will be the apex name. 
        base_ship_name = re.sub( r"([A-Z])", r"", ship_name)
        
        ship_embed_title = img_get_ship_title(self, ship_name)
        embed_colour = get_em_colour(base_ship_name)
        embed = discord.Embed(title=ship_embed_title
        , colour=embed_colour)
        embed.set_image(url=get_ship_image(ship_name))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ImgageCog(bot))
