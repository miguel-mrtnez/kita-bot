import os

from discord import Intents, Game
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Bot(BotBase):
    def __init__(self):
        super().__init__(command_prefix=os.environ['BOT_PREFIX'], 
                         owner_ids=os.environ['BOT_OWNERS_IDS'],
                         intents=Intents.all()
                         )
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

    def run(self):
        self.token = os.environ['BOT_TOKEN']
        print('launching bot...')
        super().run(self.token, reconnect=True)

    async def on_connect(self):
        # What happends on connection.
        await self.change_presence(activity=Game(name='<help'))
        print('bot connected')

    async def on_disconnected(self):
        # Whats happends on disconnection.
        print('bot disconnected')

    async def on_error(self, error, *args, **kwargs):
        if error == 'on_command_error':
            await args[0].send('Something went wrong')

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            pass
        elif hasattr(exception, 'original'):
            raise exception.original
        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(os.environ['GUILD_ID'])
        else:
            print('bot reconnected')

    # async def on_message(self, message):
    #     pass
    # Controls what happends when a message with every message sent.
