import inspect

from discord.ext import commands
from res.mods import mod_aura, mod_ship, mod_weapon, mod_zen


class ModCog(commands.Cog, name="Mod Commands"):
    """ModCog"""

    def __init__(self, client):
        self.client = client

    @commands.hybrid_group(invoke_without_command=True)
    @commands.guild_only()
    async def Mods(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        if ctx.invoked_subcommand is None and arg1 is None:
            await ctx.send("Invalid Mod command passed.")
        else:
            await ctx.send(embed=Mods(ctx, sc, arg1).p_embed())

    @Mods.command(aliases=["weapons"])
    async def weapon(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Mods(ctx, sc, arg1).p_embed())

    @Mods.command(aliases=["auras"])
    async def aura(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Mods(ctx, sc, arg1).p_embed())

    @Mods.command(aliases=["zens"])
    async def zen(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Mods(ctx, sc, arg1).p_embed())

    @Mods.command(aliases=["apexes"])
    async def apex(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=ModMods(ctx, sc, arg1).p_embed())


# The setup function below is necessary. Remember we give client.add_cog() the
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(ModCog(client))
