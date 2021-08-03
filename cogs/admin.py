from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    async def _clear(self, ctx, limit):
        with ctx.channel.typing():
            await ctx.channel.purge(limit=int(limit) + 1)
