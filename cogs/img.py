#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
import sqlite3
from discord.ext import commands
from discord.utils import get
from fuzzywuzzy import process, fuzz
from img_func import img_get_ship_title, get_em_colour
from ship_func import get_ship_image
from common import sanitise_input, ship_search
import re


def sql_name_list_obj():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info find the ship 
    c.execute('''
    select name, IfNull(null, '') as rank from s_info
    union
    select name, rank from s_apex;
    ''')
    # return the ship object including the required elemnts
    s_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return s_obj

def sql_ship_obj():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info collect all table info 
    c.execute('select * from s_info')
    # return the ship object including the required elemnts
    s_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return s_obj

def img_ship_list():
    return [f"{str(sanitise_input(i['name'])).lower()}{str(i['rank'])}" for i in sql_name_list_obj()]
        
def img_ship_search(find_this):
    # extractOne will find the single best match above a score in a list of choices
    found_this = process.extractOne(find_this, img_ship_list(), scorer=fuzz.token_sort_ratio)
    ship_name = found_this[0]
    return ship_name



class ImgageCog(commands.Cog, name="Imgage Commands"):
    """ImgageCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='img2')
    @commands.guild_only()
    # arg1 is everthing after the command
    async def img2(self, ctx, *, arg1):
        i_obj = sql_name_list_obj()
        s_obj = sql_ship_obj()
        
        base_ship_name = re.sub( r"([A-Z])", r"", img_ship_search(arg1))
        ship_name = ship_search(base_ship_name)
        # For the formatting reasons we need the base ship name so we can search
        # against other JSON files. This strips all upper case letters which
        # will be the apex name. 
        print(ship_name)
        print(base_ship_name)
        print(f'{"#"*2} {arg1} \n {"-"*40}')

        ship_embed_title = img_get_ship_title(self, ship_name)
        embed_colour = int(s_obj[ship_name]['colour'], 16)
        embed = discord.Embed(title=ship_embed_title
        , colour=embed_colour)
        embed.set_image(url=get_ship_image(ship_name))
        await ctx.send(embed=embed)


    @commands.command(name='img')
    @commands.guild_only()
    # arg1 is everthing after the command
    async def img(self, ctx, *, arg1):


        ship_name = img_ship_search(re.sub(r' ','', arg1))
        base_ship_name = re.sub( r"([A-Z])", r"", ship_name)
        ship_embed_title = img_get_ship_title(self, ship_name)
        embed_colour = get_em_colour(base_ship_name)
        embed = discord.Embed(title=ship_embed_title
        , colour=embed_colour)
        embed.set_image(url=get_ship_image(ship_name))
        imgvar = get_ship_image(ship_name)
        print(imgvar)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ImgageCog(bot))
