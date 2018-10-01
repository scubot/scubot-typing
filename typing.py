import discord
from modules.botModule import *
from tinydb import TinyDB, Query


class Typing(BotModule):
    name = 'typing'

    description = 'Simulates typing'

    help_text = ''

    trigger_string = ''

    has_background_loop = True

    module_version = '1.0.0'

    async def parse_command(self, message, client):
        if message.channel.id in self.admin_modules:
            # First time init
            if len(self.module_db) != 0:
                self.module_db.insert({'send_typing': False})
            else:
                boolean = self.module_db.all[0]['send_typing']
                self.module_db.update({'send_typing': not boolean}, Query().send_typing == boolean)
        else:
            return 0

    async def background_loop(self, client):
        await client.wait_until_ready()
        channel = client.get_channel(self.channel)
        if self.module_db.all[0]['send_typing']:
            client.send_typing(channel)
        else:
            pass
