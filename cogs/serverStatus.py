import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup as BS
import requests
import re

class ServerStatus(commands.Cog):
    WEST_AMERICA = 0
    EAST_AMERICA = 1
    WEST_EUROPE = 2
    CENTRAL_EUROPE = 3
    SOUTH_AMERICA = 4
    
    def __init__(self, client):
        self.client : commands.Bot = client
        #self.arkServerStatLoop.start()

    #@arkServerStat.before_loop
    #async def bot_ready(self):
    #    await self.client.wait_until_ready()

    @commands.command(aliases = ['arkstart'])
    async def arkServerStatStart(self, ctx: commands.Context, region=CENTRAL_EUROPE):
        print("Starting loop")
        self.arkServerStatLoop.start(ctx, region)

    @commands.command(aliases = ['arkstop'])
    async def arkServerStatStop(self, ctx: commands.Context):
        print("Stopping loop")
        self.arkServerStatLoop.stop()

    @tasks.loop(minutes=5)
    #@commands.command(aliases = ['ark'])
    async def arkServerStatLoop(self, ctx: commands.Context, region):
        '''checks the server status of a region default central europe. 
        can be changed to look att other regions
        '''
        URL = "https://www.playlostark.com/en-gb/support/server-status"

        page = requests.get(URL)
        soup = BS(page.text, 'html.parser')

        #find all server regions
        server_region = soup.find_all(class_=re.compile("(ags-ServerStatus-content-responses-response ags-ServerStatus-content-responses-response--centered)"))
        
        #skip all regions exept region 'default europe' and find all servers
        servers = server_region[region].find_all("div", class_='ags-ServerStatus-content-responses-response-server')
        
        server_name_list = ""
        server_status_list = ""

        for server in servers:
            server_name = server.find('div', class_='ags-ServerStatus-content-responses-response-server-name')

            if server.find('div', class_='ags-ServerStatus-content-responses-response-server-status--good'):
                server_status = 'Good ✅'
            if server.find('div', class_='ags-ServerStatus-content-responses-response-server-status--busy'):
                server_status = 'Busy ❌'
            if server.find('div', class_='ags-ServerStatus-content-responses-response-server-status--full'):
                server_status = 'Full ⚠️'
            if server.find('div', class_='ags-ServerStatus-content-responses-response-server-status--maintenance'):
                server_status = 'Maintenamce 🛠️'

            print(server_name.text.strip() + " " + server_status)
            server_name_list += (server_name.text.strip() + "\n")
            server_status_list += (server_status + '\n')

        server_embed = discord.Embed(title="Server status europe", colour=discord.Colour.blue(), url=URL)
        server_embed.add_field(name="Server name", value=server_name_list, inline=True)
        server_embed.add_field(name="Server status", value=server_status_list, inline=True)

        await ctx.send(embed=server_embed)

def setup(client):
    client.add_cog(ServerStatus(client))
