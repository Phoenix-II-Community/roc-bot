#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 
import re
import discord.ext.commands
from discord.ext.commands import Bot
import urllib.parse
from datetime import datetime, timezone
from common import customemoji, ship_search, sanitise_input


class Mission():
    def __init__(self, bot_self, sub_command):
        self.sub_com = sub_command
        self.bot_self = bot_self
        self.mission_epoch = 1326
        self.thumb_url = 'https://cdn.discordapp.com/attachments/340802325277048832/573289243229552640/praise.png'
        self.d_obj = self.sql_daily_obj()
        self.m_obj = self.sql_missionlist_obj()
        self.embed_daily = self.daily_embed()
        self.embed_d_list = self.d_list_embed()
    
    def sql_daily_obj(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # return a class sqlite3.row object which requires a tuple input query
        conn.row_factory = sqlite3.Row
        # make an sqlite connection object
        c = conn.cursor()
        # using a defined view s_info find the ship 
        c.execute('select * from m_daily where day = ?', (self.day_number(),))
        # return the daily mission object including the required elemnts
        sql_obj = c.fetchone()
        # close the databse connection
        conn.close()
        # return the sqlite3.cursor object
        return sql_obj

    def sql_missionlist_obj(self):
        # connect to the sqlite database
        conn = sqlite3.connect('rocbot.sqlite')
        # return a class sqlite3.row object which requires a tuple input query
        #conn.row_factory = sqlite3.Row
        # make an sqlite connection object
        c = conn.cursor()
        # using a defined view s_info find the ship
        c.execute('select * from m_daily')
        # return the list of all missions
        sql_obj = c.fetchall()
        # close the databse connection
        conn.close()
        # return the sqlite3.cursor object
        return sql_obj

    def daily_embed(self):
        title = self.d_obj['map'].upper()
        desc = self.get_daily_description_info()
        col = int(self.d_obj['colour'], 16)
        embed = discord.Embed(title=title, description=desc, colour=col)
        embed.set_footer(text=f"Day {self.d_obj['id']}") 
        embed.set_thumbnail(url=self.thumb_url)
        return embed

    def get_daily_description_info(self):
        turrets = self.d_obj['emoji']
        t_list = turrets.split()
        emoji = [str(customemoji(self.bot_self, x)) for x in t_list]
        embed_description = (
            f"Daily Mission #{self.mission_number()}\n"
            f"Invaders: {self.d_obj['inavders'].title()} {customemoji(self.bot_self, self.d_obj['inavders'])}\n"
            f"Turrets: {' '.join(emoji)}\n"
            f"Description: {self.d_obj['turrets']}"
        )
        return embed_description

    # daily mission number takes the epoch date 19/aug/2019 and performs a delta
    # against the current UTC time because the game servers change mission
    # in UTC time. Funcing uses aware values. 
    def mission_number(self):
        if self.sub_com == 'next':
            return (self.mission_epoch + 1) + (datetime.now(timezone.utc) - datetime(2019,8,19,0,0,0, tzinfo=timezone.utc)).days
        else:
            return self.mission_epoch + (datetime.now(timezone.utc) - datetime(2019,8,19,0,0,0, tzinfo=timezone.utc)).days


    # The game current has a 21 mission rotation. Based on an offset start date 
    # because the first day is indexed (start date is actually 2019/aug/19)
    # This will give us the position of the mission rotation in UTC time 
    # because that's what the game servers use. Funcing uses aware values.
    def day_number(self):
        if self.sub_com == 'next':
            day = int((datetime.now(timezone.utc) - datetime(2019,8,18,0,0,0, tzinfo=timezone.utc)).days) + 1
            #print(day % 21)
            return day % 21
        else:
            #print((datetime.now(timezone.utc) - datetime(2019,8,18,0,0,0, tzinfo=timezone.utc)).days % 21)
            return (datetime.now(timezone.utc) - datetime(2019,8,18,0,0,0, tzinfo=timezone.utc)).days % 21

    def d_list_embed(self):
        title = 'DAILY CYCLE ORDER'
        desc = self.get_d_list_description_info()
        col = int('3598DC',16)
        embed = discord.Embed(title=title, description=desc, colour=col)
        embed.set_thumbnail(url=self.thumb_url)
        return embed

    def get_d_list_description_info(self):
        embed_description = ""
        #self.m_object is a tuple object where values are accessed by index rather than column name. Access by column name only works if the database connection remains open. Will need to see if there is a way around this for readability
        col = {'id': 0, 'day': 1, 'invaders': 2, 'affinity' : 3, 'map' : 4, 'map_abbrev' : 5, 'turrets' : 6,  'emoji': 7, 'colour' :8}
        for row in self.m_obj:
            embed_description += (               f"{customemoji(self.bot_self, row[col['invaders']])} **{row[col['id']]}.** {row[col['map_abbrev']]} : {row[col['affinity']]} {row[col['turrets']]}\n")
        return embed_description

        
        
        
