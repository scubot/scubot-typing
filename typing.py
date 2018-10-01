import discord
from modules.botModule import *
from tinydb import TinyDB, Query
import asyncio


class Typing(BotModule):
    name = 'typing'

    description = 'Simulates typing.'

    help_text = '`!typing` to simulate scubot typing.'

    trigger_string = 'typing'

    has_background_loop = True

    module_version = '1.0.0'

    channel = '349851272465088513'

    async def parse_command(self, message, client):
        if message.channel.id in self.admin_modules:
            # First time init
            if len(self.module_db) == 0:
                self.module_db.insert({'send_typing': False})
                boolean = False
            else:
                boolean = self.module_db.all()[0]['send_typing']
                self.module_db.update({'send_typing': not boolean}, Query().send_typing == boolean)
            await client.send_message(message.channel, "Typing is now " + str(not boolean))
        else:
            return 0

    async def background_loop(self, client):
        await client.wait_until_ready()
        channel = client.get_channel(self.channel)
        while not client.is_closed:
            try:
                if self.module_db.all()[0]['send_typing']:
                    await client.send_typing(channel)
                else:
                    pass
            except IndexError:
                pass
            # Each 'send_typing' lasts for 10 seconds. To make it look continuous, we'll send it
            # every 8 seconds.
            await asyncio.sleep(5)
