import inspect

from discord.ext import commands

from res.apex import embed_apex_rank, embed_apex_rank_list


class ApexCog(commands.Cog, name="apex"):
    """ApexCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Apex cog loaded...")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def apex(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        if ctx.invoked_subcommand is None and arg1 is None:
            await ctx.send("Invalid Apex command passed.")
        else:
            await ctx.send("you")

    @apex.command(name="rank", help=" list of APEXs of a specific rank")
    @commands.guild_only()
    async def rank(self, ctx, *, ship=None, rank=None):
        if rank is None:
            await embed_apex_rank_list(ctx)
        else:
            await embed_apex_rank(self, ctx, rank, ship)


# The setup function below is necessary. Remember we give client.add_cog() the
# name of the class in this case ShipCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(ApexCog(client))
