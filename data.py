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
class Data():
    def __init__(self, bot_self, find_this):
        self.bot_self = bot_self
        self.ship_name = ship_search(find_this)
        self.s_obj = self.sql_ship_obj()
        self.img_url = self.get_ship_image()
        self.embed_info = self.info_embed(bot_self, find_this)
        self.embed_detail = self.detail_embed(bot_self, find_this)

    def sql_ship_obj(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # return a class sqlite3.row object which requires a tuple input query
        conn.row_factory = sqlite3.Row
        # make an sqlite connection object
        c = conn.cursor()
        # using a defined view s_info find the ship 
        c.execute('select * from s_info where name = ?', (self.ship_name,))
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

    # The embed is made up of two sections of content the title and this section
    # the descriotion. The description contains weapon, aura and zen info using 
    # an emoji followed by the relevant name of the section. 
    #
    # The description previously used format() instead f strings bceause at the 
    # time I didn't see how f strings were suited to json and dicts however 
    # since using a class that's changed and f strings seemed clearer to read. 
    def get_ship_description_info(self):
        embed_description = (
            f"{customemoji(self.bot_self, 'dps')} {self.s_obj['dmg']}\n"
            f"{customemoji(self.bot_self, self.s_obj['affinity'])} {self.s_obj['weapon_name']}\n" 
            f"{customemoji(self.bot_self, self.s_obj['aura'])} {self.s_obj['aura']}\n"
            f"{customemoji(self.bot_self, self.s_obj['zen'])} {self.s_obj['zen']}")
        return embed_description
    
    def get_ship_description_detail(self):
        embed_description = (
            f"{customemoji(self.bot_self, 'dps')} {self.s_obj['dmg']}\n"
            f"{customemoji(self.bot_self, self.s_obj['affinity'])} {self.s_obj['weapon_name']}")
        return embed_description

    def get_ship_image(self):
        urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/img/"
        img_url = (f"{urlgit}{sanitise_input(self.ship_name.lower())}.png")
        return img_url
        
    # create a discod embed object. Using the Ship class to collect the required 
    # data. The embed includes a title as a ship emoji and the ship name queried
    # The description is a combination of weapon, aura and zen names with emojis
    # to suit. weapon zen gets a generic dps emoji and zen|aura get the specific 
    # emoji 
    def info_embed(self, bot_self, find_this):
        title = self.get_ship_title()
        desc = self.get_ship_description_info()
        col = int(self.s_obj['colour'], 16)
        return discord.Embed(title=title, 
        description=desc, colour=col).set_thumbnail(url=self.img_url)


    def detail_embed(self, bot_self, ship_name):
        title = self.get_ship_title()
        desc = self.get_ship_description_detail()
        col = int(self.s_obj['colour'], 16)
        embed = discord.Embed(title=title, description=desc, colour=col)
        embed.add_field(
            name=f"{customemoji(self.bot_self, self.s_obj['aura'])} {self.s_obj['aura']}",
            value=f"{self.s_obj['aura_desc']}", 
            inline=False)
        embed.add_field(
            name=f"{customemoji(self.bot_self, self.s_obj['zen'])} {self.s_obj['zen']}",
            value=f"{self.s_obj['zen_desc']}", 
            inline=False)
        embed.add_field(
            name=f"{customemoji(self.bot_self, 'apex')} Apexs",
            value=f"{self.s_obj['zen_desc']}", 
            inline=False)
        embed.set_thumbnail(url=self.img_url)
        return embed