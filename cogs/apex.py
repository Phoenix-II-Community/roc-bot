from discord.ext import commands

from res.apex import (
    embed_apex_mod_list,
    embed_apex_rank_list,
    embed_apex_ranks,
    embed_apex_search_list,
)


class ApexCog(commands.Cog, name="Apexs"):
    """ApexCog"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Apex cog loaded...")

    @commands.hybrid_group(
        invoke_without_command=True, help=" Ships Apexs or Apex details"
    )
    @commands.guild_only()
    async def apex(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid apex command passed.")

    @apex.command(name="rank", help="Apex cost brakcets or all ships by apex rank")
    @commands.guild_only()
    async def rank(self, ctx, *, rank=None):
        if rank is None:
            await embed_apex_ranks(ctx)
        else:
            await embed_apex_rank_list(self, ctx, rank)

    @apex.command(name="mod", help="Find ships with an apex mod (eg. shield breaker)")
    @commands.guild_only()
    async def mod(self, ctx, *, type=None):
        if type is None:
            await ctx.send("Need a mod for example, shield breaker.")
        else:
            await embed_apex_mod_list(self, ctx, type)

    @apex.command(name="search", help=" list apexs for a specific ship")
    @commands.guild_only()
    async def search(self, ctx, *, ship=None, apex=None, aura=None, zen=None):
        if apex is None:
            await embed_apex_ranks(ctx)
        else:
            await embed_apex_search_list(self, ctx, ship, apex, aura, zen)


# The setup function below is necessary. Remember we give client.add_cog() the
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(ApexCog(client))
