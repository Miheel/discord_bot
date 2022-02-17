import discord
from discord.ext import commands
from bs4 import BeautifulSoup as BS
import requests
import re

WEEK_DAYS = ["Mån", "Tis", "Ons", "Tors", "Fre"]
#time edit url
URL = ""

class School(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command(aliases = ["day"])
    async def schedule(self, ctx: commands.Context, nr_days = 1):
        page = requests.get(URL)
        soup = BS(page.text, 'html.parser')

        day_list = []
        day_courses = ""
        found_days = 0

        days = soup.find_all(class_=re.compile("(headline t|time tt|columnLine)"))
        days = list(filter(len, days))
        for day_field in range(len(days)):

            for day in WEEK_DAYS:

                if days[day_field + 1].get_text().startswith(day):
                    day_list.append(day_courses + days[day_field].get_text())     

                if days[day_field].get_text().startswith(day):
                    found_days += 1
                    day_courses = ""                    

            if (found_days > nr_days):
                break             

            day_courses += days[day_field].get_text() + "\n"

        await ctx.send(embed=self.prepare_schedule(day_list))


    def prepare_schedule(self, day_list):
        embed = discord.Embed(title="Schedule", colour=discord.Colour.blue(), url=URL)
        for day in day_list:
            name = day[:day.index("\n")]
            course = day[day.index("\n"):]
            embed.add_field(name=name, value=course, inline=False)

        return embed

def setup(client):
    client.add_cog(School(client))
