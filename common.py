#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from fuzzywuzzy import process
import unicodedata
import re
import discord.ext.commands

# Connect to the local sqlite database `rocbot.sqlite` and generate a list of 
# ship names from the `ship` table
def get_ships():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples 
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    ship_list = c.execute('''SELECT name FROM ship''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return ship_list

# return the ship name from name_list which is a list of ship names 
# extracted from the databases table called ship
def ship_search(find_this):
    # using the class initiated list ship_list find one ship name that 
    # matches the given string as close as possible
    found_this = process.extractOne(find_this, get_ships())
    # fuzzywuzzy returns the name and the ratio so strip the ratio and keep 
    # the ship name
    ship_name = found_this[0]
    # return the ship name as a string
    return ship_name

# Connect to the local sqlite database `rocbot.sqlite` and generate a list of 
# invader names from the invaders table
def get_invaders():
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

def invader_search(find_this):
    if find_this != None:
        # using the class initiated list ship_list find one ship name that 
        # matches the given string as close as possible
        found_this = process.extractOne(find_this, get_invaders())
        # fuzzywuzzy returns the name and the ratio so strip the ratio and keep 
        # the ship name
        invader_name = found_this[0]
        # return the ship name as a string
        return invader_name
    else:
        pass

# strip all non lete
def sanitise_input(input_string):
    words_only = re.sub(r'\W+','', input_string)
    return unicodedata.normalize('NFKD', words_only).encode('ascii', 'ignore').decode('utf8')

def customemoji(self, find_this):
    print(f"{find_this}   ------------------------")
    if isinstance(find_this, str):
        find_sanitised = sanitise_input(find_this.lower())
        return discord.utils.get(self.bot.emojis, name = find_sanitised)
    else:
        return discord.utils.get(self.bot.emojis, name = "dps")
#def ship_command_embed_pager(self, found_this, sub_command):
#    paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
#    for ship_line in ship_command_common_list(self, found_this, sub_command):
#        paginator.add_line(ship_line)
#    return paginator.pages
#
#def element_finder(find_this, sub_command):
#    return process.extractOne(shortcuts(find_this), make_element_set(sub_command))[0]

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

def ship_command_embed_pager(self, found_this, sub_command):
    paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
    for ship_line in ship_command_common_list(self, found_this, sub_command):
        paginator.add_line(ship_line)
    return paginator.pages

def shortcut_obj():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view shortcut collect all table info 
    c.execute('select * from shortcut')
    # return the shortcut object including the required elemnts
    sc_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return sc_obj
