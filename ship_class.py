#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import sqlite3 
import re

# This replaces the old ship.py 
class ShipInfo():
    def __init__(self, find_this):
        self.ship_name = common.ship_search(find_this)
        self.s_obj = self.sql_ship_obj()
        self.embed = self.create_emebed()
        self.sanitise_input = self.sanitise_input()
    
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
        ship_title = (f"{customemoji(self.s_obj['rarity'])} {self.s_obj['name']}")
        return ship_title
    
    def get_ship_description_info(self):
        ship_description_info = (
            f"{customemoji('dps')} {self.s_obj['dmg']}\n"
            f"{customemoji(self.s_obj['affinity'])} {self.s_obj['weapon_name']}\n" 
            f"{customemoji(self.s_obj['aura'])} {self.s_obj['aura']}\n"
            f"{customemoji(self.s_obj['zen'])} {self.s_obj['zen']}\n")
        return ship_description_info
    
    def create_emebed(self):
        ship_embed_title = get_ship_title(self, self.ship_name)
        ship_embed_description = get_ship_description_info(self, self.ship_name)
        embed_colour = self.s_obj['colour']
        embed = discord.Embed(title=ship_embed_title, 
        description=ship_embed_description, colour=embed_colour)
        embed.set_thumbnail(url=get_ship_image(self.ship_name))
        return embed
