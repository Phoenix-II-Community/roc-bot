# -*- coding: utf-8 -*-

from res.common import customemoji, ship_search, argument_parser, get_em_colour, embed_pagination
import discord.ext.commands
import random
import res.sqlite_util as sqlite_util

# 2019-12-16 This class connects to rocbot.sqlite and uses a view to query. The returned
# data is put into an object where methods run uses this info to generate a
# title, image url, and description which contains emojis. The emoji function
# uses the Bot instance to perform a lookup which is why it's passed through.
# Because Discord doesn't allow non alpha characters in emojis there's a
# sanitise function that strips unwanted characters which is also used on the
# url formatting function. That's technical debt from when this was originally
# using json files instead of sqlite and the sub context of the query and name
# was used as the name to find image files, so they had to match. This isn't the
# case anymore and might be better to edit the image names now.

# 2024-01-07
# Before the bot would make one or more sqlite queries per command. As part of
# breaking out the query functions from the formatting the data that's used for those
# functions will now live in memory as a python object. There are some draw backs to this.
# Notably if a change is made to the database the python object will be out of sync so
# there needs to be manual intervention either via command or restarting the bot to resync things.
# This may mean queries are returned quicker as we're not going to disk. However, I have no
# before and after times right now to quantify that nor do I have experience performing
# accurate measuring of performance.
# --------------- SQLITE ----------------------------
# Possible Sqlite views include
# i_hp; invader hp
# m_daily; mission daily
# s_apex; ship apexs
# s_info; ship info
# shortcut; list of shortcuts for auras, zens weapon affinity, and rarity


ships_all = sqlite_util.sql_ship_info_obj()
# apexs_all = sqlite_util.sql_ship_info_obj('s_apex')
# mission_daily = sqlite_util.sql_ship_info_obj('m_daily')
# invader_stats = sqlite_util.sql_ship_info_obj('i_hp')
# shortcuts = sqlite_util.sql_ship_info_obj('shortcut')

"""
Except for the detail command the embeds used have the same basic parts.
Title; Top line of embed text that has an emoji followed by text.
Description; main section of text like the body of an email.
add_field; used to append additional title and descriptions so aura/zen formatting is consistent
Color; the left vertical line of the embed
Footer; tiny subtext used in almost all roc-bot commands
image; large image used with the img command, placed inline
thumbnail (small image) that's right aligned used in info and detail
"""

def embed_title(self, bot_self, sub_command):
    if sub_command == "affinity":
        return f"{customemoji(bot_self, 'damage')} Main Weapon Affinities"
    elif sub_command == "dmg":
        return f"{customemoji(bot_self, 'dps')} Damage Brackets"
    elif sub_command == "aura":
        return f"{customemoji(bot_self, 'aura')} Auras"
    elif sub_command == "zen":
        return f"{customemoji(bot_self, 'zen')} Zens"
    elif sub_command == "rarity":
        return f"{customemoji(bot_self, 'vegemite')} Rarities"

class ShipData():
    def __init__(self, bot_self, find_this):
        self.bot_self = bot_self
        self.ship_name = ship_search(find_this)
        self.s_obj = self.ship_obj()
        self.img_url = self.get_ship_image()
        self.embed_info = self.info_embed(find_this)
        self.embed_detail = self.detail_embed(find_this)

    def ship_obj(self):
            for s_obj in ships_all:
                if s_obj['name'] == self.ship_name:
                    return s_obj

    # Creates the title of the discord emebed consisting of the rarity emoji
    # the ship name.
    def get_ship_title(self):
        return f"{customemoji(self.bot_self, self.s_obj['rarity'])} {self.s_obj['name']}"
   
    # The embed is made up of two sections of content the title and this section
    # the description. The description contains weapon, aura and zen info using
    # an emoji followed by the relevant name of the section.
    #
    # The description previously used format() instead f strings because at the
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
        urlgit = "https://raw.githubusercontent.com/Phoenix-II-Community/roc-bot/master/ships/"
        return f"{urlgit}ship_{self.s_obj['number']}.png"
       
    # create a discod embed object. Using the Ship class to collect the required
    # data. The embed includes a title as a ship emoji and the ship name queried
    # The description is a combination of weapon, aura and zen names with emojis
    # to suit. weapon zen gets a generic dps emoji and zen|aura get the specific
    # emoji
    def info_embed(self, find_this):
        title = self.get_ship_title()
        desc = self.get_ship_description_info()
        col = int(self.s_obj['colour'], 16)
        embed = discord.Embed(title=title,
                              description=desc,
                              colour=col).set_thumbnail(url=self.img_url)
        embed.set_footer(text=f"Ship {self.s_obj[0]}")
        return embed
       
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
        embed.set_footer(text=f"Ship {self.s_obj['number']}")
        return embed
class ShipLister():
    def __init__(self, bot_self, ctx, arg1, sc):
        self.bot_self = bot_self
        self.ctx = ctx
        self.arg1 = argument_parser(sc, arg1)
        self.sub_command = sc
        self.embed_title = self.title()
        self.s_obj = self.ship_obj()

    def ship_obj(self):
        if self.sub_command in ('all', 'rand'):
            return ships_all
        else:
            s_obj = []
            for i in ships_all:
                if i[self.sub_command] == self.arg1:
                    s_obj.append(i)
        return s_obj

    def create_description(self):
        description = []
        if self.sub_command == 'dmg':
            for i in self.s_obj:
                description.append(
                    f"{customemoji(self.bot_self, i['affinity'])} "
                    f"{customemoji(self.bot_self, i['name'])} "
                    f"{i['name']}")
            return embed_pagination(description)
        elif self.sub_command == 'affinity':
            for i in self.s_obj:
                description.append(
                    f"{customemoji(self.bot_self, i['name'])} "
                    f"{i['name']}")
            return embed_pagination(description)
        elif self.sub_command == 'rand':
            for i in self.s_obj:
                description.append(
                    f"{customemoji(self.bot_self, i['affinity'])} "
                    f"{customemoji(self.bot_self, i['name'])} "
                    f"{i['name']}")
            return embed_pagination(random.sample(description, int(self.arg1)))
        # having an else without knowing what uses it sucks
        else:
            for i in self.s_obj:
                description.append(
                    f"{customemoji(self.bot_self, i['affinity'])} "
                    f"{customemoji(self.bot_self, i['name'])} "
                    f"{i['name']}")
            return embed_pagination(description)

    async def create_embed(self):
        ctx = self.ctx
        if self.sub_command == 'affinity':
            colour = get_em_colour(self.arg1)
            for page in self.create_description():
                await ctx.send(embed=discord.Embed(
                    title=self.embed_title,
                    description=page,
                    color=colour))
        else:
            for page in self.create_description():
                await ctx.send(embed=discord.Embed(
                    title=self.embed_title,
                    description=page))

    def title(self):
        if self.sub_command == "dmg":
            return f"{customemoji(self.bot_self, 'dps')} {self.arg1} DPS Ships"
        if self.sub_command == "all":
            return "All Ship Listing"
        if self.sub_command == "rand":
            return f"Random list of {self.arg1} ships"
        else:
            return f"{customemoji(self.bot_self, self.arg1)} {self.arg1} Ships"

class CategoryLister():
    def __init__(self, bot_self, sub_command):
        self.bot_self = bot_self
        self.sub_command = sub_command
        self.s_obj = ships_all
        self.embed_list = self.create_list()

    def create_list(self):
        new_set = set({})
        list1 = []
        for i in self.s_obj:
            new_set.add(i[self.sub_command])
        for i in sorted(new_set):
            if self.sub_command == 'dmg':
                list1.append(f"{i}")
            else:
                list1.append(f"{customemoji(self.bot_self, i)} {i}")
        description = '\n'.join(list1)
        embed = discord.Embed(
            title=embed_title(self, self.bot_self, self.sub_command),
            description=description)
        return embed




