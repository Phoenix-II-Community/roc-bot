#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
import sqlite3
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from rapidfuzz import process, fuzz
import re
from res.common import sanitise_input, ship_search, customemoji
from res.data import ShipData


def sql_apex_num_obj():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info find the ship 
    c.execute('''
select
    ship.id as id,
    apex_tier.name as rank,
    apex_ships.apex_num as apex_num
from apex_ships inner join ship on apex_ships.ship_name = ship.id
inner join apexs on apex_ships.apex_id = apexs.id
inner join apex_tier on apex_ships.apex_tier = apex_tier.id;
    ''')
    # return the ship object including the required elemnts
    a_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return a_obj

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

def get_ship_image(ship_name):
    urlgit = "https://raw.githubusercontent.com/Phoenix-II-Community/roc-bot/master/ships/"
    return f"{urlgit}ship_{ship_name}.png"

@app_commands.guild_only()
class ImageCog(commands.Cog, name="Image Commands"):
    """ImgageCog"""
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Image cog loaded...')

    @commands.hybrid_command(name='img')
    @commands.guild_only()
    # ship_name is everything after the command
    async def img(self, ctx, *, ship_name):
        rank_list = [i[0] for i in sql_rank_obj()]
        res = [i for i in rank_list if i.lower() in ship_name.lower()]
        if len(res) == 0:
            s_obj = ShipData(self, ship_name).s_obj
            ship_embed_title = f"{customemoji(self, s_obj['rarity'])} {s_obj['name']}"
            col = int(s_obj['colour'], 16)
            embed = discord.Embed(
                title=ship_embed_title,
                colour=col)
            embed.set_image(url=get_ship_image(s_obj['number']))
            embed.set_footer(text=f"Ship {s_obj['number']}")
            await ctx.send(embed=embed)
        else:
            a_obj = sql_apex_num_obj()
            s_obj = ShipData(self, ship_name).s_obj
            for i in a_obj:
                if i['id'] == s_obj['number'] and i['rank'] == res[0]:
                    ship_embed_title = f"{customemoji(self, s_obj['rarity'])} {s_obj['name']} {res[0]}"
                    col = int(s_obj['colour'], 16)
                    embed = discord.Embed(title=ship_embed_title, colour=col)
                    embed.set_image(url=get_ship_image(f"{i['id']}_apex_{i['apex_num']}"))
                    embed.set_footer(text=f"Ship {s_obj['number']}")
                    await ctx.send(embed=embed)

async def setup(client) -> None:
    await client.add_cog(ImageCog(client))
