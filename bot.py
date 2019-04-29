#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import settings
import discord
from discord.ext import commands
import json


# Create variable json_data assign the opening of a file to it
ships_json=open('res/ships.json')
print(ships_json)
ships_data = json.load(ships_json)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()

bot = commands.Bot(command_prefix='!')

#@bot.command(pass_context=True)
#async def test(ctx, arg1):
#    await ctx.send('here {}'.ships)

@bot.command()
async def ships(ctx, arg1):
    for element in ships_data[arg1]:
        await ctx.send(element['ship_name'] + "\n" + \
                       ":" + element['damage type']  + ":" + "\n" + \
                       str(element['damage output']) + "\n" + \
                       element['weapon_name'] + "\n" + \
                       element['aura'] + "\n" + \
                       element['zen'] + "\n" + \
                       ":" + element['r'] + ":")
        return

@bot.command()
async def invaders(ctx, arg1):
    for element in jdata[arg1]:
        await ctx.send(element['ship_name'] + "\n" + \
                        ":" + element['damage type']  + ":" + "\n" + \
                        str(element['damage output']) + "\n" + \
                        element['weapon_name'] + "\n" + \
                        element['aura'] + "\n" + \
                        element['zen'] + "\n" + \
                        ":" + element['r'] + ":")
        return


bot.run(settings.discordkey)
