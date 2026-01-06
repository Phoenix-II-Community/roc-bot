import inspect

from discord.ext import commands

from res.apex import ApexApexs, Apexs


class ApexCog(commands.Cog, name="Apex Commands"):
    """ApexCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def Apex(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        if ctx.invoked_subcommand is None and arg1 is None:
            await ctx.send("Invalid Apex command passed.")
        else:
            await ctx.send(embed=Apexs(ctx, sc, arg1).p_embed())

    @Apex.command(aliases=["weapons"])
    async def weapon(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Apexs(ctx, sc, arg1).p_embed())

    @Apex.command(aliases=["auras"])
    async def aura(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Apexs(ctx, sc, arg1).p_embed())

    @Apex.command(aliases=["zens"])
    async def zen(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=Apexs(ctx, sc, arg1).p_embed())

    @Apex.command(aliases=["apexes"])
    async def apex(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=ApexApexs(ctx, sc, arg1).p_embed())
