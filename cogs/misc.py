import discord
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is ready')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'pong! {round(self.client.latency * 1000)} ms')

    @commands.command(aliases = ['cls', 'c'])
    async def clear(self, ctx: commands.Context, amount = 2):
        await ctx.channel.purge(limit = amount)

def setup(client):
    client.add_cog(Misc(client))
