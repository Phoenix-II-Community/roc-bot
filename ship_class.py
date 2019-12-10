#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common import customemoji, ship_search
import sqlite3 
import re
import discord.ext.commands
from discord.ext.commands import Bot

# This replaces the old ship.py 
class ShipInfo(Bot):
    def __init__(self, bot_self, find_this):
        self.bot_self = bot_self
        self.ship_name = ship_search(find_this)
        self.s_obj = self.sql_ship_obj()
        self.embed = self.create_emebed()
        self.embed_title = self.get_ship_title()
        self.embed_description = self.get_ship_description_info()
        self.ship_image = self.get_ship_image()

    def sql_ship_obj(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # return a class sqlite3.row object which requires a tuple input query
        conn.row_factory = sqlite3.Row
        # make an sqlite connection object
        c = conn.cursor()
        # using a defined view s_info find the ship 
        c.execute('select * from s_info where name = ?', self.ship_name)
        # return the ship object including the required elemnts
        ship_obj = c.fetchone()
        # close the databse connection
        conn.close()
        # return the sqlite3.cursor object
        return ship_obj

    # Creates the title of the discord emebed consisting of the rarity emoji 
    # the ship name.
    def get_ship_title(self):
        ship_title = (f"{customemoji(self.bot_self, self.s_obj['rarity'])} {self.s_obj['name']}")
        return ship_title
    
    def get_ship_description_info(self):
        ship_description_info = (
            f"{customemoji(self.bot_self, 'dps')} {self.s_obj['dmg']}\n"
            f"{customemoji(self.bot_self, self.s_obj['affinity'])} {self.s_obj['weapon_name']}\n" 
            f"{customemoji(self.bot_self, self.s_obj['aura'])} {self.s_obj['aura']}\n"
            f"{customemoji(self.bot_self, self.s_obj['zen'])} {self.s_obj['zen']}\n")
        return ship_description_info
    
    def get_ship_image(self):
        urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/img/"
        url = ("{giturl}{shipname}.png").format(giturl=urlgit, shipname=self.ship_name)
        return url

    def create_emebed(self):
        embed = discord.Embed(title=self.embed_title, 
        description=self.embed_description, colour=self.s_obj['colour'])
        embed.set_thumbnail(url=self.ship_image)
        return embed
