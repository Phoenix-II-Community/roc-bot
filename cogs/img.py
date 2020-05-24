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
from data import ShipData
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
    select
        ship.name,
        apex_tier.name as rank,
        ship.id as ship_id,
        apex_ships.apex_num as apex_num
        from apex_ships inner join ship on apex_ships.ship_name = ship.id
        inner join apexs on apex_ships.apex_id = apexs.id
        inner join apex_tier on apex_ships.apex_tier = apex_tier.id
        inner join apex_type on apexs.apex_type_id = apex_type.id
        inner join ship_aura on ship.aura_id=ship_aura.id
    union
    select
        ship.name,
        IfNull(null, '') as rank,
        ship.id as ship_id,
        IfNull(null, '') as ship_apex
        from ship;
    ''')
    # return the ship object including the required elemnts
    s_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return s_obj

def sql_ship_obj():
    conn = sqlite3.connect('rocbot.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from s_info')
    s_obj = c.fetchall()
    conn.close()
    return s_obj

def sql_rank_obj():
    conn = sqlite3.connect('rocbot.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select name from apex_tier')
    r_obj = c.fetchall()
    conn.close()
    return r_obj

def img_ship_list():
    return [f"{str(sanitise_input(i['name'])).lower()}{str(i['rank'])}" for i in sql_name_list_obj()]
        
def img_ship_search(find_this):
    # extractOne will find the single best match above a score in a list of choices
    found_this = process.extractOne(find_this, img_ship_list(), scorer=fuzz.token_sort_ratio)
    ship_name = found_this[0]
    return ship_name

def get_ship_image2(ship_name):
    urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/ships/"
    url = f"{giturl}'ship_'{shipname}.png"
    return url

class ImgageCog(commands.Cog, name="Imgage Commands"):
    """ImgageCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='img2')
    @commands.guild_only()
    # arg1 is everthing after the command
    async def img2(self, ctx, *, arg1):
        rank_list = [i[0] for i in sql_rank_obj()]
        res = [i for i in rank_list if i.lower() in arg1.lower()] 
        s_obj = sql_ship_obj()
        #i_obj = sql_name_list_obj()
        if len(res) =< 0:
            s_obj = ShipData(ctx, arg1).s_obj

        #base_ship_name = re.sub( r"([A-Z])", r"", img_ship_search(arg1))
        #ship_name = ship_search(base_ship_name)

            ship_embed_title = s_obj['name']
            col = int(s_obj['colour'], 16)
            embed = discord.Embed(title=ship_embed_title
            , colour=embed_colour)
            embed.set_image(url=get_ship_image2(ship_name))
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
