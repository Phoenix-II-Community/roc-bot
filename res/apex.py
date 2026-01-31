import discord.ext.commands
from rapidfuzz import process

from res.common import customemoji, get_em_colour, sanitise_input
from res.data import (
    apex_price,
    apex_ships,
    apex_tier,
    apex_types,
    aura_names,
    ship_names,
    zen_names,
)
from res.sqlite_util import sql_apex_num_obj, sql_apex_obj, sql_apex_search


async def embed_apex_ranks(ctx):
    description = []
    for i in apex_price:
        description.append(f"{i['name']}: {i['cost']}")
    embed = discord.Embed(title="Apex ranks", description="\n".join(description))
    await ctx.send(embed=embed)


def find_apex_type(a):
    apex_type = None
    if a["type"] == "aura":
        apex_type = a["aura"]
    if a["type"] == "zen":
        apex_type = a["zen"]
    if a["type"] == "weapon":
        apex_type = "damage"
    return apex_type


async def embed_apex_rank_list(self, ctx, rank):
    # :highimpact~1: :tarcahLAMBDA: Tar'Cah LAMBDA - :pointdefense: (¢30000)
    apex_rank = process.extractOne(rank.upper(), apex_tier)[0]
    description = []
    title = f"{apex_rank} Apexes - ¢35000"
    for i in apex_ships:
        if i["rank"] == apex_rank:
            ship_apex = sanitise_input(i["name"].lower() + i["rank"].upper())
            type = find_apex_type(i)
            emoji_type = customemoji(self, type)
            emoji_apex = discord.utils.get(self.client.emojis, name=ship_apex)
            emoji_affinity = customemoji(self, i["affinity"])
            description.append(
                f"{emoji_affinity} {emoji_apex} {i['name']} {i['apex']} {emoji_type}"
            )
    embed = discord.Embed(title=title, description="\n".join(description))
    await ctx.send(embed=embed)


async def embed_apex_rank_list(self, ctx, wpn, aura, zen):
    # :highimpact~1: :tarcahLAMBDA: Tar'Cah LAMBDA - :pointdefense: (¢30000)
    apex_rank = process.extractOne(rank.upper(), apex_tier)[0]
    description = []
    title = f"{apex_rank} Apexes - ¢35000"
    for i in apex_ships:
        if i["rank"] == apex_rank:
            ship_apex = sanitise_input(i["name"].lower() + i["rank"].upper())
            type = find_apex_type(i)
            emoji_type = customemoji(self, type)
            emoji_apex = discord.utils.get(self.client.emojis, name=ship_apex)
            emoji_affinity = customemoji(self, i["affinity"])
            description.append(
                f"{emoji_affinity} {emoji_apex} {i['name']} {i['apex']} {emoji_type}"
            )
    embed = discord.Embed(title=title, description="\n".join(description))
    await ctx.send(embed=embed)


async def embed_apex_mod_list(self, ctx, mod):
    # :highimpact~1: :tarcahLAMBDA: Tar'Cah LAMBDA - :pointdefense: (¢30000)
    find = mod.title()
    print(find)
    print(apex_types)
    apex_type = process.extractOne(find, apex_types)[0]
    description = []
    title = f"Ship Apexes with {apex_type}"
    for i in apex_ships:
        if i["apex"] == apex_type:
            ship_apex = sanitise_input(i["name"].lower() + i["rank"].upper())
            type = find_apex_type(i)
            emoji_type = customemoji(self, type)
            emoji_apex = discord.utils.get(self.client.emojis, name=ship_apex)
            emoji_affinity = customemoji(self, i["affinity"])
            description.append(
                f"{emoji_affinity} {emoji_apex} {i['name']} {i['rank']} {emoji_type} (¢{i['cost']})"
            )
    embed = discord.Embed(title=title, description="\n".join(description))
    await ctx.send(embed=embed)


async def embed_apex_search_list(self, ctx, ship=None, mod=None, aura=None, zen=None):
    """Search apexes with flexible filtering."""

    if not any([ship, mod, aura, zen]):
        await ctx.send("Please provide at least one filter: ship, mod, aura, or zen")
        return

    filters_applied = []

    if ship:
        ship = process.extractOne(ship, ship_names)[0]
        filters_applied.append(f"Ship: {ship}")

    if mod:
        mod = process.extractOne(mod.title(), apex_types)[0]
        filters_applied.append(f"Mod: {mod}")

    if aura:
        aura = process.extractOne(aura.title(), aura_names)[0]
        filters_applied.append(f"Aura: {aura}")

    if zen:
        zen = process.extractOne(zen.title(), zen_names)[0]
        filters_applied.append(f"Zen: {zen}")

    results = sql_apex_search(ship=ship, mod=mod, aura=aura, zen=zen)

    if not results:
        await ctx.send(f"No apexes found matching: {', '.join(filters_applied)}")
        return

    description = []
    for i in results:
        # {affinity emoji} {ship emoji} Ship name Apex name (aura/zen/weapon emoji)
        ship_apex = sanitise_input(i["name"].lower() + i["rank"].upper())
        emoji_apex = discord.utils.get(self.client.emojis, name=ship_apex)
        emoji_affinity = customemoji(self, i["affinity"])
        emoji_ability = customemoji(self, i["apex_ability"])
        description.append(
            f"{emoji_affinity} {emoji_apex} {i['name']} {i['apex']} {emoji_ability}"
        )

    title = f"Apex Search: {', '.join(filters_applied)}"
    embed = discord.Embed(title=title, description="\n".join(description))
    await ctx.send(embed=embed)


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
