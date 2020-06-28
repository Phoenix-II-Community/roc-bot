#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from invader_func import invader_type_list, invader_embed
from ship_func import get_ship_title, get_em_colour, get_ship_image
from common import customemoji
from rapidfuzz import process, fuzz
import re
import os
import json


cwd = os.getcwd()
imgsrch_json = open(f'{cwd}/res/imgsrch.json')
imgsrch_data = json.load(imgsrch_json)
ships_json = open(f'{cwd}/res/ships.json')
ships_data = json.load(ships_json)




def img_ship_search(find_this):
    print(type(find_this))
    found_this = process.extractOne(find_this, imgsrch_data, scorer=fuzz.token_sort_ratio)
    print(found_this)
    ship_name = found_this[0]
    return ship_name

def img_get_ship_title(self, ship_name):
    base_ship_name = re.sub( r"([A-Z])", r"", ship_name)
    ship_dict = ships_data[base_ship_name]
    ship_title = ("{rarityemoji} {nameofship}").format(\
        rarityemoji=customemoji(self, ship_dict["rarity"]), 
        # the regex inserts a space before the first upper case letter 
        nameofship=re.sub( r"([A-Z]+)", r" \1", ship_name))
    return ship_title
