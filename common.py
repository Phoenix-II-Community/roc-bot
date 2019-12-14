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

# strip all non lete
def sanitise_input(input_string):
    words_only = re.sub(r'\W+','', input_string)
    return unicodedata.normalize('NFKD', words_only).encode('ascii', 'ignore').decode('utf8')

def customemoji(self, find_this):
    find_sanitised = sanitise_input(find_this.lower())
    return discord.utils.get(self.bot.emojis, name = find_sanitised)
