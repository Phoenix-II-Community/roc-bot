import discord
import discord.ext.commands
from discord.ext import commands
from discord import app_commands
from res.common import sanitise_input, ship_search, customemoji
from res.data import apex_tier, apex_num
from res.common import ShipData


def get_ship_image(ship_name):
    urlgit = "https://raw.githubusercontent.com/Phoenix-II-Community/roc-bot/master/ships/"
    return f"{urlgit}ship_{ship_name}.png"

@app_commands.guild_only()
class ImageCog(commands.Cog, name="Image Commands"):
    """ImgageCog"""
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Image cog loaded...')

    @commands.hybrid_command(name='img')
    @commands.guild_only()
    # ship_name is everything after the command
    async def img(self, ctx, *, ship_name):
        rank_list = [i[0] for i in apex_tier]
        res = [i for i in rank_list if i.lower() in ship_name.lower()]
        if len(res) == 0:
            print("*** len = 0")
            s_obj = ShipData(self, ship_name).s_obj
            ship_embed_title = f"{customemoji(self, s_obj['rarity'])} {s_obj['name']}"
            col = int(s_obj['colour'], 16)
            embed = discord.Embed(
                title=ship_embed_title,
                colour=col)
            embed.set_image(url=get_ship_image(s_obj['number']))
            embed.set_footer(text=f"Ship {s_obj['number']}")
            await ctx.send(embed=embed)
        else:
            print("*** ELSE")
            s_obj = ShipData(self, ship_name).s_obj
            for i in apex_num:
                if i['id'] == s_obj['number'] and i['rank'] == res[0]:
                    ship_embed_title = f"{customemoji(self, s_obj['rarity'])} {s_obj['name']} {res[0]}"
                    col = int(s_obj['colour'], 16)
                    embed = discord.Embed(title=ship_embed_title, colour=col)
                    embed.set_image(url=get_ship_image(f"{i['id']}_apex_{i['apex_num']}"))
                    embed.set_footer(text=f"Ship {s_obj['number']}")
                    await ctx.send(embed=embed)

async def setup(client) -> None:
    await client.add_cog(ImageCog(client))