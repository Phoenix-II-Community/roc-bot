from discord.ext import commands

from res.invaders import get_i_embed


class InvaderCog(commands.Cog, group_name="Invader Commands"):
    """InvaderCog"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Invader cog loaded...")

    @commands.hybrid_group(invoke_without_command=True, aliases=["invaders"])
    @commands.guild_only()
    async def invader(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid invader command passed.")

    ############################################################################
    # invader ship class
    ############################################################################

    @invader.command()
    async def roc(self, ctx):
        sc = ctx.command.name
        print(sc)
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def condor(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def vulture(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def eagle(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def heron(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def raven(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def sparrow(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    ############################################################################
    # invader build class
    ############################################################################

    @invader.command()
    async def unprotected(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def armored(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def shielded(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    @invader.command()
    async def split(self, ctx):
        sc = ctx.command.name
        await ctx.send(embed=get_i_embed(self, sc))

    ############################################################################
    # invader turrets info graphic
    ############################################################################

    @invader.command()
    async def turrets(self, ctx):
        await ctx.send("Feature coming soon")


async def setup(client) -> None:
    await client.add_cog(InvaderCog(client))
