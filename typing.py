from discord.ext import commands, tasks
from tinydb import TinyDB, Query
import asyncio
import discord

class Typing(commands.Cog):
    def __init__(self, bot):
        self.version = "2.0.0"
        self.bot = bot
        self.channel = None
        self.db = TinyDB('./modules/databases/typing')
        self.background_loop.start()

    @tasks.loop(seconds=5.0)
    async def background_loop(self):
        try:
            if self.db.all()[0]['send_typing'] and self.channel is not None:
                await self.channel.trigger_typing()
            else:
                pass
        except IndexError:
            pass

    @background_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.background_loop.cancel()

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.command()
    async def typing(self, ctx):
        # First time init
        if len(self.db) == 0:
            self.db.insert({'send_typing': False})
            boolean = False
        else:
            boolean = self.db.all()[0]['send_typing']
            self.db.update({'send_typing': not boolean}, Query().send_typing == boolean)
        self.channel = ctx.channel
        await ctx.send("Typing is now " + str(not boolean))


def setup(bot):
    bot.add_cog(Typing(bot))
