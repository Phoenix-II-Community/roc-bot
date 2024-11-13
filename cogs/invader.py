from discord.ext import commands
from res.invaders import invader_type

class InvaderCog(commands.Cog, group_name="Invader Commands"):
    """InvaderCog"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Invader cog loaded...')

    @commands.hybrid_group(invoke_without_command=True, aliases=['invaders'])
    @commands.guild_only()
    async def invader(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        if ctx.invoked_subcommand is None and arg1 is None:
            await ctx.send('Invalid invader command passed.')
        else:
            await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def turrets(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def unprotected(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def armored(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def shielded(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def split(self, ctx, *, arg1=None):
        sc = ctx.subcommand_passed
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

async def setup(client) -> None:
    await client.add_cog(InvaderCog(client))
