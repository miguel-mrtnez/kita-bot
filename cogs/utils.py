from random import shuffle, choice, randint

from discord.ext import commands
from discord import Embed


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='teams')
    async def _teams(self, ctx, n, *args):
        try:
            n = int(n)
        except:
            await ctx.send('Ingresa el número de teams')
        teams = [[] for x in range(n)]

        if n > len(args):
            await ctx.send('El número de teams supera al número de players')
        
        else:
            people = list(args)
            shuffle(people)

            i = 0
            while people:
                teams[i].append(people.pop())
                i += 1
                if i == n:
                    i = 0
        
            message = Embed(color=0xFF0000)
            for team in range(n):
                name, value = (f'Team {team + 1}', '\n '.join(teams[team]))
                message.add_field(name=name, value=value, inline=False)
        
            await ctx.send(embed=message)

    @commands.command(name='coin')
    async def _coin(self, ctx):
        sides = {
            'fase': '<:coin_face:803747204090167296>',
            'tail': '<:coin_tail:803747228702343188>'
        }
        
        result = choice(['fase', 'tail'])
        await ctx.send(sides[result])

    @commands.command(name='dice')
    async def _dice(self, ctx):
        faces = {
            1: '<:dice_1:802710831698673674>',
            2: '<:dice_2:802710889143861249>',
            3: '<:dice_3:802710908836905000>',
            4: '<:dice_4:802710926222295040>',
            5: '<:dice_5:802710944059752489>',
            6: '<:dice_6:802710962683641897>'
        }
        
        result = randint(1, 6)
        await ctx.send(faces[result])

    @commands.command(name='choice')
    async def _choice(self, ctx, *args):
        
        await ctx.send(choice(args))
