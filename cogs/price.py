import inspect

from discord.ext import commands

from res.price import ApexPrices, Prices


class PriceCog(commands.Cog, name="Price Commands"):
    """PriceCog"""

    def __init__(self, client):
        self.client = client

    @commands.hybrid_group(invoke_without_command=True)
    @commands.guild_only()
    async def price(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        if ctx.invoked_subcommand is None and arg1 is None:
            await ctx.send("Invalid price command passed.")
        else:
            await ctx.send(embed=Prices(ctx, sc, arg1).p_embed())

    @price.command(aliases=["weapons"])
    async def weapon(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Prices(ctx, sc, arg1).p_embed())

    @price.command(aliases=["auras"])
    async def aura(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Prices(ctx, sc, arg1).p_embed())

    @price.command(aliases=["zens"])
    async def zen(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Prices(ctx, sc, arg1).p_embed())

    @price.command(aliases=["apexes"])
    async def apex(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=ApexPrices(ctx, sc, arg1).p_embed())


async def setup(client) -> None:
    await client.add_cog(PriceCog(client))
