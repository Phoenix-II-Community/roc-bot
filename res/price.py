# -*- coding: utf-8 -*-
import discord.ext.commands
from res.data import apex_price
from res.sqlite_util import sql_p_s_obj


class Prices:
    def __init__(self, bot_self, sub_command, arg1):
        # self.sc = sub_command
        self.bot = bot_self
        self.type = arg1
        self.p_obj = sql_p_s_obj(sub_command)

    def p_embed(self):
        desc = ""
        for row in self.p_obj:
            desc = desc + str(row["Level"]) + " - " + row["Cost"] + "\n"
        embed = discord.Embed(title="Level" + "\t" + "Cost", description=desc)
        return embed


class ApexPrices:
    def __init__(self, bot_self, sub_command, arg1):
        self.sc = sub_command
        self.bot = bot_self
        self.type = arg1
        self.p_obj = apex_price

    def p_embed(self):
        desc = ""
        for row in self.p_obj:
            desc = f"{desc}{str(row['name'])} - {row['cost']:,}\xa2 \n"
        embed = discord.Embed(title="Level" + "\t" + "Cost", description=desc)
        return embed
