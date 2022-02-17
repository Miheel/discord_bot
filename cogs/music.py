import discord
from discord.errors import ClientException
from discord.ext import commands
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True
    }

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
    }

ydl = youtube_dl.YoutubeDL(ydl_opts)



class Music(commands.Cog):
    
    def __init__(self, client):
         self.client: commands.Bot = client

    @commands.command()
    async def join(self, ctx: commands.Context):
        try:
            Voice_channel = ctx.author.voice.channel
            await Voice_channel.connect()
        except ClientException:
            await ctx.send(f'Bot already connected to a chanel')

    @commands.command()
    async def leave(self, ctx: commands.Context):
        try:
            await ctx.voice_client.disconnect()
        except AttributeError:
            await ctx.send(f'Bot is not connected')

    @commands.command()
    async def play(self, ctx: commands.Context, song = None):
        try:
            Voice_channel = ctx.author.voice.channel
            await Voice_channel.connect()
        except ClientException:
            pass
        finally:
            data = ydl.extract_info(song, download=False)
            url = data['formats'][0]['url']
            ctx.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))

    @commands.command()
    async def stop(self, ctx: commands.Context):
        await ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx: commands.Context):
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx: commands.Context):
        await ctx.voice_client.resume()

    @play.before_invoke
    async def check(self, ctx: commands.Context):
        if ctx.voice_client == None:
            pass
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(client):
    client.add_cog(Music(client))
