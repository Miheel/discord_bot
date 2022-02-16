import discord
from discord.ext import commands
from bs4 import BeautifulSoup as BS
import requests
import re

class ServerStatus(commands.Cog):
    WEST_AMERICA = 0
    EAST_AMERICA = 1
    CENTRAL_EUROPE = 2
    SOUTH_AMERICA = 3
    
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['ark'])
    async def arkServerStat(self, ctx, region=CENTRAL_EUROPE):
        '''checks the server status of a region default central europe. 
        can be changed to look att other regions
        '''
        URL = "https://www.playlostark.com/en-gb/support/server-status"

        page = requests.get(URL)
        soup = BS(page.text, 'html.parser')

        #find all server regions
        server_region = soup.find_all(class_=re.compile("(ags-ServerStatus-content-responses-response ags-ServerStatus-content-responses-response--centered)"))
        
        #skip all regions exept 3rg region 'default europe' and find all servers
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
