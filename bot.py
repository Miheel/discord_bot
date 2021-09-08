import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix = '!')

@client.command()
async def load(ctx, extension = None):
    if (extension == None):
        load_all_ext()
        await ctx.send(f'Loaded all cogs')
    else:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded cog {extension}')

@load.error
async def load_error(ctx, error):
    await ctx.send(f'The following error occured\n{error}')

@client.command(aliases = ['uload'])
async def unload(ctx, extension = None):
    if (extension == None):

        unload_all_ext()
        await ctx.send(f'Unloaded all cogs')
    else:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded cog {extension}')

@unload.error
async def unload_error(ctx, error):
    await ctx.send(f'The following error occured\n{error}')

@client.command(aliases = ['rload'])
async def reload(ctx, extension = None):
    if (extension == None):
        unload_all_ext()
        load_all_ext()
        await ctx.send(f'Reloaded all cogs')
    else:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded cog {extension}')

@reload.error
async def reload_error(ctx, error):
    await ctx.send(f'The following error occured\n{error}')


def load_all_ext():
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            client.load_extension(f'cogs.{file_name[:-3]}')

def unload_all_ext():
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            client.unload_extension(f'cogs.{file_name[:-3]}')

def main():
    load_all_ext()
    client.run(TOKEN)

if __name__ == '__main__':
    main()
