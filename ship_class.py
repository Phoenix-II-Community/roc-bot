#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common import customemoji, ship_search, sanitise_input
import sqlite3 
import re
import discord.ext.commands
from discord.ext.commands import Bot
import urllib.parse

# This class connects to rocbot.sqlite and uses a view to query. The returned 
# data is put into an object where methods run uses this info to generate a
# title, image url, and description which contains emojis. The emoji function 
# uses the Bot instance to perform a lookup which is why it's passed through.
# Because Discord doesn't allow non alpha characters in emojis there's a 
# santise function that strips unwanted characters which is also used on the 
# url formatting function. That's technical debt from when this was orignally
# using json files instead of sqlite and the sub context of the query and name 
# was used as the name to find image files so they had to match. This isn't the 
# case anymore and might be better to edit the image names now. 
class Ship():
    def __init__(self, bot_self, find_this):
        self.bot_self = bot_self
        self.ship_name = ship_search(find_this)
        self.s_obj = self.sql_ship_obj()
        self.img_url = self.get_ship_image()

    def sql_ship_obj(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # return a class sqlite3.row object which requires a tuple input query
        conn.row_factory = sqlite3.Row
        # make an sqlite connection object
        c = conn.cursor()
        # using a defined view s_info find the ship 
        c.execute('select * from s_info where name = ?', [self.ship_name])
        # return the ship object including the required elemnts
        s_obj = c.fetchone()
        # close the databse connection
        conn.close()
        # return the sqlite3.cursor object
        return s_obj

    # Creates the title of the discord emebed consisting of the rarity emoji 
    # the ship name.
    def get_ship_title(self):
        embed_title = (
            f"{customemoji(self.bot_self, self.s_obj['rarity'])} {self.s_obj['name']}")
        return embed_title
    
    def get_ship_description_info(self):
        embed_description = (
            f"{customemoji(self.bot_self, 'dps')} {self.s_obj['dmg']}\n"
            f"{customemoji(self.bot_self, self.s_obj['affinity'])} {self.s_obj['weapon_name']}\n" 
            f"{customemoji(self.bot_self, self.s_obj['aura'])} {self.s_obj['aura']}\n"
            f"{customemoji(self.bot_self, self.s_obj['zen'])} {self.s_obj['zen']}")
        return embed_description
    
    def get_ship_image(self):
        urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/img/"
        img_url = (f"{urlgit}{sanitise_input(self.ship_name.lower())}.png")
        return img_url

# create a discod embed object. Using the Ship class to collect the required data
def info_embed(bot_self, find_this):
    info = Ship(bot_self, find_this)
    title = info.get_ship_title()
    desc = info.get_ship_description_info()
    col = int(info.s_obj['colour'], 16)
    return discord.Embed(title=title, 
    description=desc, colour=col).set_thumbnail(url=info.img_url)

