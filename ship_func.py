#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################
####                    !ship Functions                     ####
################################################################
from fuzzywuzzy import process
from pathlib import Path
import json
import re
import unicodedata
import random
import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
import settings
import os

# Open the required json files and assign it to a variable foo_data
cwd = os.getcwd()
ships_json = open(f'{cwd}/res/ships.json')
ships_data = json.load(ships_json)
shortcuts_json = open(f'{cwd}/res/shortcuts.json')
shortcuts_data = json.load(shortcuts_json)
auras_json = open(f'{cwd}/res/auras.json')
auras_data = json.load(auras_json)
zens_json = open(f'{cwd}/res/zens.json')
zens_data = json.load(zens_json)


embed_colours = {"Shield Breaker": 0x3a77f9, "High Impact": 0xee4529, "Armor Piercing": 0xffb820}

# return the ship name from ships_data using the last value
# the last value is the ship name 
def ship_search(find_this):
    found_this = process.extractOne(find_this, ships_data.keys())
    ship_name = found_this[0]
    return ship_name

# Discord embed have a line of the left hand side. This line can be coloured
# This function uses one of the 3 affinity choices to select a colour from
# the embed_colours variable (red/yellow/blue)
def get_em_colour(ship_name):
    ship_dict = ships_data[ship_name]
    dmg_type = ship_dict["affinity"]
    em_colour = embed_colours[dmg_type]
    return em_colour

def get_detail_aura_value(aura):
    aura_dict = auras_data[aura]
    list1 = []
    for k, v in aura_dict.items():
        list1.append(("{key} {value}").format(key=k, value=v))
    return '\n'.join(list1)
    
def get_detail_zen_value(zen):
    zen_dict = zens_data[zen]
    list1 = []
    for k, v in zen_dict.items():
        list1.append(("{key} {value}").format(key=k, value=v))
    return '\n'.join(list1)

def get_detail_value_zen(self, ship_name):
    ship_dict = ships_data[ship_name]
    zen_title = ("{emoji} {zen}").format(\
        emoji=customemoji(self, ship_dict["zen"]), 
        zen=ship_dict["zen"])
    return zen_title

def get_detail_value_aura(self, ship_name):
    ship_dict = ships_data[ship_name]
    aura_title = ("{emoji} {zen}").format(\
        emoji=customemoji(self, ship_dict["aura"]), 
        zen=ship_dict["aura"])
    return aura_title

def info_embed(self, ship_name):
    ship_embed_title = get_ship_title(self, ship_name)
    ship_embed_description = get_ship_description_info(self, ship_name)
    embed_colour = get_em_colour(ship_name)
    embed = discord.Embed(title=ship_embed_title, 
    description=ship_embed_description, colour=embed_colour)
    embed.set_thumbnail(url=get_ship_image(ship_name))
    return embed


def detail_embed(self, ship_name):
    ship_embed_title = get_ship_title(self, ship_name)
    ship_embed_description = get_ship_description_detail(self, ship_name)
    embed_colour = get_em_colour(ship_name)
    embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
    embed.add_field(name=get_detail_value_aura(self, ship_name), value=get_detail_aura_value(ships_data[ship_name]['aura']), inline=False)
    embed.add_field(name=get_detail_value_zen(self, ship_name), value=get_detail_zen_value(ships_data[ship_name]['zen']), inline=False)
    embed.set_thumbnail(url=get_ship_image(ship_name))
    return embed

# This is the small embed description output used by the
#  "!ship info <ship name>" command. 
def get_ship_description_info(self, ship_name):
    ship_dict = ships_data[ship_name]
    ship_description_info = ("{emojidps} {ship[dmg]}\n"
    "{emojidmgtype} {ship[weapon_name]}\n"
    "{emojiaura} {ship[aura]}\n"
    "{emojizen} {ship[zen]}\n").format(emojidps=customemoji(self, "dps"),
            emojidmgtype=customemoji(self, ship_dict["affinity"]),
            emojiaura=customemoji(self, ship_dict["aura"]),
            emojizen=customemoji(self, ship_dict["zen"]),
            ship=ship_dict)
    return ship_description_info


# This is the small embed description output used by the
#  "!ship detail <ship name>" command. 
def get_ship_description_detail(self, ship_name):
    ship_dict = ships_data[ship_name]
    ship_description_detail = ("{emojidps} {ship[dmg]}\n"
    "{emojidmgtype} {ship[weapon_name]}\n").format(emojidps=customemoji(self, "dps"),
            emojidmgtype=customemoji(self, ship_dict["affinity"]),
            ship=ship_dict)
    return ship_description_detail


# Each ship has a number based on the in game order they were listed and added.
# return that100% number. 
def find_number(ship_name):
    ship_dict = ships_data[ship_name]
    number = ship_dict["number"]
    return number

# Creates the title of the discord emebed consisting of the rarity emoji 
# the ship name.
def get_ship_title(self, ship_name):
    ship_dict = ships_data[ship_name]
    ship_title = ("{rarityemoji} {nameofship}").format(\
        rarityemoji=customemoji(self, ship_dict["rarity"]), 
        nameofship=ship_dict["ship_name"])
    return ship_title

def get_ship_image(ship_name):
    urlgit = "https://github.com/Phoenix-II-Community/apex-bot/raw/master/img/"
    url = ("{giturl}{shipname}.png").format(giturl=urlgit, shipname=ship_name)
    return url



# Making a set of elements found based on the sub command string that's used.
# The sub command string matches a ship.json key.  
def make_element_set(sub_command):
    new_set = set({})
    for elements in ships_data.values():
        new_set.add(elements[sub_command])
    return sorted(new_set)

# shortcuts.json is imported and used as shortcuts_data
def shortcuts(find_this):
    if find_this in shortcuts_data:
        return shortcuts_data[find_this]
    else:
        return find_this

def finder(find_this, sub_command):
    return process.extractOne(shortcuts(find_this), make_element_set(sub_command))[0]

# A standard list used by many funcitons to output a list 
# affinity emoji, ship emoji, ship name. 
def ship_command_common_title(self, found_this, sub_command):
    if sub_command == "dmg":
        var_title = ("{dpsemoji} DPS {dps}").format(dpsemoji=customemoji(self, "dps"), \
            dps=found_this)
    else:
        var_title = ("{emoji} {context} Ships").format(emoji=customemoji(self, found_this), \
            context=found_this)
    return var_title


def ship_command_common_list(self, found_this, sub_command):
    list1 = []
    for elements in ships_data.values():
        if elements[sub_command] == found_this:
            list1.append(("{elementemoji} {shipemoji} {name}").format(\
                elementemoji=customemoji(self, elements['affinity']), \
                shipemoji=customemoji(self, elements['ship_name'].lower()),\
                name=elements['ship_name']))
    return (list1)


def ship_command_embed_pager(self, found_this, sub_command):
    paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
    for ship_line in ship_command_common_list(self, found_this, sub_command):
        paginator.add_line(ship_line)
    return paginator.pages


async def generic_ship_command_embed(self, ctx, arg1, sub_command):
    found_this = finder(arg1, sub_command)
    title = ship_command_common_title(self, found_this, sub_command)
    for page in ship_command_embed_pager(self, found_this, sub_command):
        await ctx.send(embed=discord.Embed(title=title, description=page))

def ship_command_random_list(self, quantity):
    list1 = []
    for elements in ships_data.values():
        list1.append(("{elementemoji} {shipemoji} {name}").format(\
            elementemoji=customemoji(self, elements['affinity']), \
            shipemoji=customemoji(self, elements['ship_name'].lower()),\
            name=elements['ship_name']))
    return random.sample(list1, int(quantity))

def random_command_embed_pager(self, quantity):
    paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
    for ship_line in ship_command_random_list(self, quantity):
        paginator.add_line(ship_line)
    return paginator.pages

async def random_ship_command_embed(self, ctx, arg1):
    title = 'Random Selection'
    for page in random_command_embed_pager(self, arg1):
        await ctx.send(embed=discord.Embed(title=title, description=page))


def ship_command_all_list(self):
    list1 = []
    for elements in ships_data.values():
        list1.append(("{elementemoji} {shipemoji} {name}").format(\
            elementemoji=customemoji(self, elements['affinity']), \
            shipemoji=customemoji(self, elements['ship_name'].lower()),\
            name=elements['ship_name']))
    return list1

def all_command_embed_pager(self):
    paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
    for ship_line in ship_command_all_list(self):
        paginator.add_line(ship_line)
    return paginator.pages

async def all_ship_command_embed(self, ctx):
    title = 'Random Selection'
    for page in all_command_embed_pager(self):
        await ctx.send(embed=discord.Embed(title=title, description=page))


def affinity_search(self, find_this, sub_command):
    list1 = []
    found_this = process.extractOne(shortcuts(find_this), make_element_set(sub_command))
    for elements in ships_data.values():
        if elements['affinity'] == found_this[0]:
            list1.append(("{emoji} {name}").format(
                emoji=customemoji(self, elements['ship_name'].lower()),
                name=elements['ship_name']))
        description = '\n'.join(list1)
        title = ("{emoji} {affinity} Ships").format(
            emoji=customemoji(self, found_this[0]), \
            affinity=found_this[0])
        em_colour = embed_colours[found_this[0]]
        embed = discord.Embed(title=title, description=description, colour=em_colour)
    return embed

def sanitise_input(input_string):
    words_only = re.sub(r'\W+','', input_string)
    return unicodedata.normalize('NFKD', words_only).encode('ascii', 'ignore').decode('utf8')

def customemoji(self, find_this):
    find_sanitised = sanitise_input(find_this.lower())
    return discord.utils.get(self.bot.emojis, name = find_sanitised)


#def auralisting(self, sub_command):
#    list1 = []
#    for elements in make_element_set(sub_command):
#        list1.append(("{emoji} {name}").format(
#            emoji=customemoji(self, elements),
#            name=elements))
#    description = '\n'.join(list1)
#    title = ("Auras")
#    return discord.Embed(title=title, description=description)
#
#def zenlisting(self, sub_command):
#    list1 = []
#    for elements in make_element_set(sub_command):
#        list1.append(("{emoji} {name}").format(
#            emoji=customemoji(self, elements),
#            name=elements))
#    description = '\n'.join(list1)
#    title = ("Zens")
#    return discord.Embed(title=title, description=description)
#
#def affinitylisting(self, sub_command):
#    list1 = []
#    for elements in make_element_set(sub_command):
#        list1.append(("{emoji} {name}").format(
#            emoji=customemoji(self, elements),
#            name=elements))
#    description = '\n'.join(list1)
#    title = ("Main Weapon Affinities")
#    return discord.Embed(title=title, description=description)
#
#def damagelisting(self, sub_command):
#    list1 = []
#    for elements in make_element_set(sub_command):
#        list1.append(("{name}").format(name=elements))
#    description = '\n'.join(list1)
#    title = ("{dpsemoji} Damage Brackets").format(dpsemoji=customemoji(self, "dps"))
#    return discord.Embed(title=title, description=description)
#
#def raritylisting(self, sub_command):
#    list1 = []
#    for elements in make_element_set(sub_command):
#        list1.append(("{emoji} {name}").format(
#            emoji=customemoji(self, elements),
#            name=elements))
#    description = '\n'.join(list1)
#    title = ("{rareemoji} Rarities").format(rareemoji=customemoji(self, "vegemite"))
#    return discord.Embed(title=title, description=description)
