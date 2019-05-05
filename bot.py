#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import settings
import discord
from discord.ext import commands
import json
from functools import partial


# Create variable json_data assign the opening of a file to it
ships_json=open('/Users/peter.carstairs/scripts/apex-bot/res/ships.json')
print(ships_json)
ships_data = json.load(ships_json)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

#@bot.command(pass_context=True)
#async def test(ctx, arg1):
#    await ctx.send('here {}'.ships)

#def ship_title(arcg1):
#   for element in ships_data[arg1]:
#       ship_name = element['ship_name']
#       rarity = element['r']
#       ship_embed_title = ship_name + " " + rarity
#       return ship_embed_title
#
#def ship_description(arg1):
#   for element in ships_data[arg1]:
#       ship_name = element['ship_name']
#       damage_output = str(element['damage output'])
#       damage_type = element['damage type']
#       weapon_name = element['weapon_name']
#       rarity = element['r']
#       ship_stats_embed_description = damage_output + damage_type + weapon_name
#       return ship_stats_embed_description
#
#def ship_aura(arg1):
#   for element in ships_data[arg1]:
#       aura = element['aura']
#       return aura
#
#def ship_zen(arg1):
#   for element in ships_data[arg1]:
#       zen = element['zen']
#       return zen



def ship_stat(ship_name, stat_name):    # <-- note, you don't have to call it arg1 in the other functions, they can
                                        # make up their own name for it that will only be used within that function,
                                        # so the code is more descriptive returns the first seen stat for the given
                                        # ship name and stat name
   for element in ships_data[ship_name]:
       stat_value = element[stat_name]
       return stat_value


def em_colour(type):
    if type == "sb":
        return 0x3a77f9
    elif type == "hi":
        return 0xee4529
    elif type == "ap":
        return 0xffb820


client = MyClient()
bot = commands.Bot(command_prefix='!')


@bot.command()
async def ships(ctx, ship_name):
    ship_embed_title = ship_stat(ship_name, "rarity") + " " + ship_stat(ship_name, "ship_name")
    ship_embed_description = ship_stat(ship_name, "aura")
    ship_embed_zen = ship_stat(ship_name, "zen")
    ship_embed_aura = ship_stat(ship_name, "aura")
    embed_colour = em_colour(ship_stat(ship_name, "damage_type"))
    embed = discord.Embed(title=ship_embed_title, description=ship_embed_description, colour=embed_colour)
    embed.add_field(name="Aura", value=ship_embed_aura, inline=False)
    embed.add_field(name="Zen", value=ship_embed_zen, inline=False)
    await ctx.send(embed=embed)
    return


@bot.command()
async def invaders(ctx, arg1):
    for element in jdata[arg1]:
        await ctx.send(element['ship_name'] + "\n" + \
                        element['damage type'] + "\n" + \
                        str(element['damage output']) + "\n" + \
                        element['weapon_name'] + "\n" + \
                        element['aura'] + "\n" + \
                        element['zen'] + "\n" + \
                        ":" + element['r'] + ":")
        return

bot.run(settings.discordkey)
