#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from rapidfuzz import process
from ship_func import customemoji
import os 
from pathlib import Path
import json

cwd = os.getcwd()
invaders_json = open(f'{cwd}/res/invaders.json')
invaders_data = json.load(invaders_json)


################################################################
####                 !invader Functions                     ####
################################################################

invaders = {"sparrow", "raven", "heron", "eagle", "vulture", "condor", "roc"}

def invader_title(sub_command):
    if sub_command == "invsplit":
        var_title = ("{invsplit} Shield and Unprotected HP Split").format(invsplit=customemoji("invsplit"))
    else:
        var_title = ("{emoji} {context} Invaders").format(emoji=customemoji(sub_command), \
            context=sub_command.capitalize())
    return var_title

def invder_search(find_this):
    found_this = process.extractOne(find_this, invaders)
    invader_name = found_this[0]
    return invader_name


def invader_type_list(arg1):
    list1 = []
    found_this = invder_search(arg1)
    for k, v in invaders_data.items():
        for kv in v.items():
            if kv[0] == found_this:
                    list1.append(("{invader} {stat}").format(invader=kv[0], stat=kv[1]))
    return '\n'.join(list1)

def get_invader_list(sub_command):
    invader_dict = invaders_data[sub_command]
    list1 = []
    for k, v in invader_dict.items():
        list1.append(("{key} {value}").format(key=k, value=v))
    return '\n'.join(list1)

def invader_embed(sub_command):
    invader_embed_title = invader_title(sub_command)
    invader_embed_description = get_invader_list(sub_command)
    embed = discord.Embed(  title=invader_embed_title, 
                            description=invader_embed_description)
    return embed

