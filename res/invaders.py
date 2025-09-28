import discord.ext.commands
from res.common import customemoji
from res.data import invader_all


def get_description(bot_self, sc):
    list1 = []
    if sc in get_invaders():
        for i in invader_all:
            if sc in i:
                list1.append(f"{customemoji(bot_self, i['type'])} {i['hp']}")
        return "\n".join(list1)
    else:
        for i in invader_all:
            if sc in i:
                list1.append(f"{customemoji(bot_self, i['name'])} {i['hp']}")
        return "\n".join(list1)


def get_title(bot_self, sc):
    return f"{customemoji(bot_self, sc)} {sc.capitalize()}"


def get_i_embed(bot_self, sc):
    em_col = {
        "shielded": 0x3A77F9,
        "unprotected": 0xEE4529,
        "armored": 0xFFB820,
        "split": 0x945E91,
    }
    title = get_title(bot_self, sc)
    desc = get_description(bot_self, sc)
    invader_names = get_invaders()
    print(invader_names)
    if sc in invader_names:
        return discord.Embed(title=title, description=desc)
    else:
        col = em_col.get(sc)
        return discord.Embed(title=title, description=desc, colour=col)
