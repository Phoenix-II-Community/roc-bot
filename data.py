#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common import customemoji, ship_search, sanitise_input, sql_ship_obj
import sqlite3 
import discord.ext.commands
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import urllib.parse
from fuzzywuzzy import process


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
class ShipData():
    def __init__(self, bot_self, find_this):
        self.bot_self = bot_self
        self.ship_name = ship_search(find_this)
        self.s_obj = self.sql_ship_obj()
        self.img_url = self.get_ship_image()
        self.embed_info = self.info_embed(find_this)
        self.embed_detail = self.detail_embed(find_this)
        
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
    def info_embed(self, find_this):
        title = self.get_ship_title()
        desc = self.get_ship_description_info()
        col = int(self.s_obj['colour'], 16)
        return discord.Embed(title=title, 
        description=desc, colour=col).set_thumbnail(url=self.img_url)
        
    def detail_embed(self, ship_name):
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
        embed.set_thumbnail(url=self.img_url)
        return embed

class ShipLister():
    if __name__ == "__main__":
        asyncio.run(main())

    def __init__(self, ship_cog, bot_self, arg1, sub_command):
        self.bot_self = bot_self
        self.sub_command = sub_command
        self.argument = arg1
        self.sc_obj = self.shortcut_obj()
        self.s_obj = sql_ship_obj()
        self.affinity = self.shortcuts()
        self.embed_list = self.create_emebed()
        
    def shortcut_obj(self):
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

    def shortcuts(self):
        if len(self.argument) <= 4:
            for i in self.sc_obj:
                if i['shortcut'] == self.argument.lower():
                    print("--------------------------------")
                    print(i['shortcut'])
                    print(i['name'])
                    print("--------------------------------")
                    return (i['name'])
        else:
            print("--------------------------------")
            print('shortcut else used')
            print("--------------------------------")
            return self.argument

    def create_set(self):
        new_set = set({})
        for i in self.s_obj:
            new_set.add(i[self.sub_command])
        return new_set

    def finder(self):
        return process.extractOne(self.shortcuts(), self.create_set())[0]

    def create_list(self):
        list1 = []
        # the damage brackets are integers or floats and also don't have emojis 
        # so the if statement accodmodates the different is data sets 
        if self.sub_command == "affinity":
            for i in sorted(self.s_obj, key=lambda k: k['number']):
                if i[self.sub_command] == self.finder():
                    list1.append(f"{customemoji(self.bot_self, i['name'])} {i['name']}")
            return list1
        else:
            for i in sorted(self.s_obj, key=lambda k: k['number']):
                if i[self.sub_command] == self.finder():
                    list1.append(f"{customemoji(self.bot_self, i['affinity'])} {customemoji(self.bot_self, i['name'])} {i['name']}")
            return list1

    def affinity_col(self):
        print('#########      affinity col')
        for i in self.sc_obj:
            if self.shortcuts() == self.affinity:
                return int(i['name'], 16)

    def make_pages(self):
        paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
        for ship_line in self.create_list():
            paginator.add_line(ship_line)
        return paginator.pages

    async def create_emebed(self):
        print('#########      create embed')
        if self.sub_command == "affinity":
            for page in self.make_pages():
                await self.bot_self.send(
                    embed=discord.Embed(title=self.ship_title(), 
                    description=page, 
                    colour=self.affinity_col()))
        else:
            for page in self.make_pages():
                await self.bot_self.send(
                    embed=discord.Embed(title=self.cat_title(), 
                    description=page))

    def cat_title(self):
        if self.sub_command == "affinity":
            return f"{customemoji(self.bot_self, 'damage')} {self.affinity} Ships"
        elif self.sub_command == "dmg":
            return f"{customemoji(self.bot_self, 'damage')} Damage Brackets"
        elif self.sub_command == "aura":
            return f"{customemoji(self.bot_self, 'aura')} {self.finder()} Ships"
        elif self.sub_command == "zen":
            return f"{customemoji(self.bot_self, 'zen')} {self.finder()} Ships"
        elif self.sub_command == "rarity":
            return f"{customemoji(self.bot_self, 'vegemite')} Rarities"
        else:
            pass

    def ship_title(self):
        if self.sub_command == "affinity":
            return f"{customemoji(self.bot_self, 'damage')} Main Weapon Affinities"
        elif self.sub_command == "dmg":
            return f"{customemoji(self.bot_self, 'damage')} Damage Brackets"
        elif self.sub_command == "aura":
            return f"{customemoji(self.bot_self, 'aura')} {self.finder()} Ships"
        elif self.sub_command == "zen":
            return f"{customemoji(self.bot_self, 'zen')} {self.finder()} Ships"
        elif self.sub_command == "rarity":
            return f"{customemoji(self.bot_self, 'vegemite')} Rarities"
        else:
            pass

class CategoryLister():
    def __init__(self, bot_self, sub_command):
        self.bot_self = bot_self
        self.sub_command = sub_command
        self.s_obj = sql_ship_obj()
        self.embed_list = self.create_list()

    def create_set(self):
        new_set = set({})
        for i in self.s_obj:
            new_set.add(i[self.sub_command])
        return new_set

    def create_list(self):
        list1 = []
        # the damage brackets are integers or floats and also don't have emojis 
        # so the if statement accodmodates the different is data sets 
        for i in sorted(self.create_set()):
            list1.append(f"{customemoji(self.bot_self, i)} {i}")
        description = '\n'.join(list1)
        return discord.Embed(title=self.title(), description=description)

    def title(self):
        if self.sub_command == "affinity":
            return f"{customemoji(self.bot_self, 'damage')} Main Weapon Affinities"
        elif self.sub_command == "dmg":
            return f"{customemoji(self.bot_self, 'damage')} Damage Brackets"
        elif self.sub_command == "aura":
            return f"{customemoji(self.bot_self, 'aura')} Auras"
        elif self.sub_command == "zen":
            return f"{customemoji(self.bot_self, 'zen')} Zens"
        elif self.sub_command == "rarity":
            return f"{customemoji(self.bot_self, 'vegemite')} Rarities"
        else:
            pass
