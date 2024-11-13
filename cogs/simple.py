import discord
from discord.ext import commands
from discord import app_commands
from discord import client
from res.common import ShipLister


class SimpleCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Simple cog loaded...')

    @commands.hybrid_command(name='repeat', description='Sends what you type')
    @commands.guild_only()
    async def do_repeat(self, ctx: commands.Context, your_input: str) -> None:
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""
        await ctx.send(your_input)

    #@commands.command(name='ping')
    #@commands.guild_only()
    #async def ping(self, ctx):
    #    await ctx.send(f"pong! {round(self.bot.discord.client.latency * 1000)}ms")

    @commands.hybrid_command(name='source', description='GitHub repository link')
    @commands.guild_only()
    async def source(self, ctx):
        src = "https://github.com/Phoenix-II-Community/apex-bot"
        await ctx.send(src)


    @commands.hybrid_command(name='rand', description='lists 10 ships or the number given')
    @commands.guild_only()
    async def rand(self, ctx, *, qty=None):
        """lists 10 ships or the number given.
        """
        sc = ctx.command.name
        if qty is None:
            qty = 10
            print(f"{sc} ## the sub command")
            print(f"{qty} ## the arg1 entry")
        if ctx.channel.id in (378546862627749908, 596343881705062417, 1166027391089512499):
            await ShipLister(self, ctx, qty, sc).create_embed()
        else:
            await ctx.send("Command limited to <#378546862627749908>.")


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
async def setup(client) -> None:
    await client.add_cog(SimpleCog(client))
