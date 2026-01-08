import discord.ext.commands
from rapidfuzz import process

from res.common import get_em_colour, sanitise_input
from res.data import apex_price
from res.sqlite_util import sql_apex_num_obj, sql_apex_obj

print(apex_price)


def embed_apex_rank():
    pass


def embed_apex_rank_list():
    pass


def apex_create_list(self):
    sql_apex_obj(self)
    description = ""
    for i in self.s_apex_obj:
        apex_type = ""
        ship_apex = sanitise_input(i["name"].lower() + i["rank"].upper())
        find_emoji = discord.utils.get(self.bot_self.bot.emojis, name=ship_apex)
        if i["type"] == "aura":
            apex_type = i["aura"]
        if i["type"] == "zen":
            apex_type = i["zen"]
        if i["type"] == "weapon":
            apex_type = "Main Weapon"
        description = f"{description} {find_emoji} {i['rank']}: {i['apex']} - {apex_type} (cost: {i['cost']:,}\xa2) \n"
    return description


async def apex(self, ctx, *, arg1):
    rank_list = [i[0] for i in sql_apex_num_obj()]
    tokens = arg1.split(" ")
    ##If no apex rank is given, show list of available apexes
    if len(tokens) == 1:
        s_obj = ships_all["tokens"]
        apex_embed_title = f"Apexes for {s_obj['name']}"
        colour = get_em_colour(s_obj["affinity"])
        embed = discord.Embed(
            title=apex_embed_title,
            description=ApexLister(ctx, arg1).embed_list,
            color=colour,
        )
        # embed.set_image(url=get_ship_image(s_obj['number']))
        await ctx.send(embed=embed)
    ##If rank is given
    else:
        a_obj = sql_apex_num_obj()
        s_obj = ShipData(ctx, arg1).s_obj
        apex_tier = process.extractOne(arg1, rank_list)[0]
        apex_obj = ApexData(ctx, s_obj["name"], apex_tier)
        colour = get_em_colour(s_obj["affinity"])
        embed = discord.Embed(
            title=apex_obj.embed_title, color=colour, description=apex_obj.embed_desc
        )
        for i in a_obj:
            if i["id"] == s_obj["number"] and i["rank"] == apex_tier:
                embed.set_thumbnail(
                    url=get_ship_image(f"{i['id']}_apex_{i['apex_num']}")
                )
        await ctx.send(embed=embed)


def find_apex_type(a):
    apex_type = None
    if a["type"] == "aura":
        apex_type = a["aura"]
    if a["type"] == "zen":
        apex_type = a["zen"]
    if a["type"] == "weapon":
        apex_type = "Main Weapon"
    return apex_type
