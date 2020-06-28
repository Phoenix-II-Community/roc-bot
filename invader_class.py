#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3 
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from common import customemoji
from rapidfuzz import process

class invader_type():
    def __init__(self, bot_self, sub_command, arg1):
        self.sc = sub_command
        self.bot_self = bot_self
        self.type = arg1
        self.i_name = self.invader_search(arg1)
        self.i_obj = self.get_sql_obj()
        self.i_embed = self.get_i_embed()

    # Connect to the local sqlite database `rocbot.sqlite` and generate a list of 
    # invader names from the invaders table
    def get_invaders(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # Return a list of items instead of 1 item tuples 
        conn.row_factory = lambda cursor, row: row[0]
        # make an sqlite connection object
        c = conn.cursor()
        # creates a variable and assigns the list of ship names to it
        invader_list = c.execute('''SELECT name FROM invaders''').fetchall()
        # close the databse connection
        conn.close()
        # return a list of ship names
        return invader_list

    def invader_search(self, find_this):
        if find_this != None:
            # using the class initiated list ship_list find one ship name that 
            # matches the given string as close as possible
            found_this = process.extractOne(find_this, self.get_invaders())
            # rapidfuzz returns the name and the ratio so strip the ratio and keep
            # the ship name
            invader_name = found_this[0]
            # return the ship name as a string
            return invader_name
        else:
            pass

    # Grab the Invader stats for a specific ship from the SQL view 
    def sql_i_name_obj(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # return a class sqlite3.row object which requires a tuple input query
        conn.row_factory = sqlite3.Row
        # make an sqlite connection object
        c = conn.cursor()
        # using a defined view s_info find the ship 
        c.execute('select * from i_hp where name = ?', (self.i_name,))
        # return the ship object including the required elemnts
        i_obj = c.fetchall()
        # close the databse connection
        conn.close()
        # return the sqlite3.cursor object
        return i_obj

    # Grab the Invader stats for a specific affinity of invader from the SQL view 
    def sql_i_type_obj(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # return a class sqlite3.row object which requires a tuple input query
        conn.row_factory = sqlite3.Row
        # make an sqlite connection object
        c = conn.cursor()
        # using a defined view s_info find the ship 
        c.execute('select * from i_hp where type = ?', (self.sc,))
        # return the ship object including the required elemnts
        i_obj = c.fetchall()
        # close the databse connection
        conn.close()
        # return the sqlite3.cursor object
        return i_obj

    def get_sql_obj(self):
        if self.sc == self.type:
            i_obj = self.sql_i_name_obj()
            return i_obj
        else:
            i_obj = self.sql_i_type_obj()
            return i_obj

    def get_description(self):
        list1 = []
        if self.sc == self.type:
            for i in self.i_obj:
                list1.append(f"{customemoji(self.bot_self, i['type'])} {i['hp']}")
            return '\n'.join(list1)
        else:
            for i in self.i_obj:
                list1.append(f"{customemoji(self.bot_self, i['name'])} {i['hp']}")
            return '\n'.join(list1)

    def get_title(self):
        if self.sc == self.type:
            return f"{customemoji(self.bot_self, self.i_name)} {self.i_name.capitalize()} HP"
        else:
            return f"{customemoji(self.bot_self, self.sc)} {self.sc.capitalize()} HP"

    def get_i_embed(self):
        em_col = {"shielded": 0x3a77f9, "unprotected": 0xee4529, "armored": 0xffb820, 'split': 0x945e91}
        title = self.get_title()
        desc = self.get_description()
        if self.sc == self.type:
            return discord.Embed(title=title, description=desc)
        else:
            col = em_col.get(self.sc) 
            return discord.Embed(title=title, description=desc, colour=col)
