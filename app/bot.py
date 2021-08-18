import os
from datetime import date

from discord import Intents, Game
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .db.birthdates import birthdates


class Bot(BotBase):
    def __init__(self):
        super().__init__(command_prefix=os.environ['BOT_PREFIX'], 
                         owner_ids=os.environ['BOT_OWNERS_IDS'],
                         intents=Intents().all()
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
            self.scheduler.add_job(self.birthday, CronTrigger(hour=0))
            self.scheduler.start()
        else:
            print('bot reconnected')

    async def birthday(self):

        today = date.today().strftime("%d-%m-%Y")
        t_day, t_month, _ = today.split('-')

        for key in birthdates:
            p_day, p_month, _ = key.split('-')
            if t_day == p_day and t_month == p_month:
                member = birthdates[key]
                channel = self.get_channel(802999675346354224)
                await channel.send(f'{self.get_user(member).mention} está de cumpleaños :partying_face:! @here')

