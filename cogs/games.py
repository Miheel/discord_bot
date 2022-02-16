import discord
from discord.ext import commands
import random


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    #commands
    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes - definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    "Don't count on it.",
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Very doubtful.']

        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(aliases = ['RPS'])
    async def rockpaperscisor(self, ctx, choice = None):
        list = ['Rock', 'Paper', 'Scissors']

        bot_choice = random.choice(list)

        outcome = f'Bot chose: {bot_choice}\nYou chose {choice}'

        if (choice == None):
            await ctx.send(f'you must pick one of the Tree {list}')
            return

        #Draw
        if (choice == bot_choice):
            await ctx.send(f"It's a draw\n{outcome}")
        #Player win
        elif (choice == 'Rock' and bot_choice == 'Scissors' or choice =='Paper' and bot_choice == 'Rock' or choice =='Scissors' and bot_choice == 'Paper'):
            await ctx.send(f'You win\n{outcome}')
        #Bot win
        else:
            await ctx.send(f'You lose\n{outcome}', tts=True)

def setup(client):
    client.add_cog(Games(client))
