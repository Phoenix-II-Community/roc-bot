# -*- coding: utf-8 -*-

from rapidfuzz import process
import unicodedata
import re
import discord.ext.commands
from discord.ext import commands
from res.data import arg_list, ships_all
import random
from res.data import damage_brackets, invader_names
from res.sqlite_util import shortcut_obj

def get_ships():
    names = []
    for i in ships_all:
        names.append(i['name'])
    return names

def ship_search(find_this):
    found_this = process.extractOne(find_this, get_ships())
    ship_name = found_this[0]
    return ship_name


def invader_search(find_this):
    if find_this != None:
        found_this = process.extractOne(find_this, invader_names)
        invader_name = found_this[0]
        return invader_name
    else:
        pass

# strip all non lete
def sanitise_input(input_string):
    # \W+ matches any non-word character (equal to [^a-zA-Z0-9_])
    # + Quantifier — Matches between one and unlimited times, as many times as 
    # possible, giving back as needed (greedy)
    words_only = re.sub(r'\W+','', str(input_string))
    return unicodedata.normalize('NFKD', words_only).encode('ascii', 'ignore').decode('utf8')


def customemoji(self, find_this):
    find_sanitised = sanitise_input(find_this.lower())
    return discord.utils.get(self.client.emojis, name = str(find_sanitised))

def embed_pagination(description):
    paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
    for ship_line in description:
        paginator.add_line(ship_line)
    return paginator.pages


def argument_parser(sc, arg1):
    clean_arg1 = sanitise_input(arg1)
    if sc == 'dmg':
        dmg_bracket = process.extractOne(clean_arg1, damage_brackets)
        return dmg_bracket[0]
    elif sc == 'rand':
        try:
            int(arg1)
        except ValueError:
            return 10
        except TypeError:
            return 10
        else:
            return arg1
    else:
        if len(clean_arg1) <= 4:
            shortcut = shortcut_obj(clean_arg1.lower())
            if len(shortcut) > 0:
                return shortcut[0]['name']
        else:
            arg_found = process.extractOne(clean_arg1, arg_list)
            return arg_found[0]

def get_em_colour(arg1):
    embed_colours = {"Shield Breaker": 0x3a77f9, "High Impact": 0xee4529, "Armor Piercing": 0xffb820}
    return embed_colours[arg1]

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
            s = self
            s_obj = []
            for i in ships_all:
                if i[s.sub_command] == s.arg1:
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


class ShipData():
    def __init__(self, bot_self, find_this):
        self.bot_self = bot_self
        self.ship_name = ship_search(find_this)
        self.s_obj = self.ship_obj()
        self.img_url = self.get_ship_image()
        self.embed_info = self.info_embed(find_this)  # <------ uses customemoji()
        self.embed_detail = self.detail_embed(find_this)  # <------ uses customemoji()

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

    # create a discord embed object. Using the Ship class to collect the required
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
