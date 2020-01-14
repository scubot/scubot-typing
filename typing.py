from discord.ext import commands, tasks
from tinydb import TinyDB, Query
import discord


class Typing(commands.Cog):
    def __init__(self, bot):
        """
        Initialise the Typing module

        Set all of the various properties of the module and its required operating variables, open the database, start
        the background loop, and initialise the database if needed.

        Args:
            bot (Bot): discord.py provided object that is used to assist with various discord interfacing
        """
        self.version = "2.0.0"
        self.bot = bot
        self.channel = None
        self.db = TinyDB('./modules/databases/typing')
        self.background_loop.start()

        # Set typing to false on startup, and initialise the database
        if len(self.db) == 0:
            self.db.insert({'send_typing': False, 'channel': None})
        else:
            self.db.update({'send_typing': False}, Query())

    @tasks.loop(seconds=5.0)
    async def background_loop(self):
        """
        Background loop for triggering typing

        When typing is triggered by discord.py it only lasts for ~8 seconds, therefore a loop is necessary to keep it
        going over an extended period, the loop runs constantly over a 5 second interval to ensure that the typing
        appears continuous. The loop runs constantly but only triggers typing if the DB entry is true.

        Examples:
            For examples and usage see: https://discordpy.readthedocs.io/en/latest/ext/tasks/
        """
        try:
            if self.db.all()[0]['send_typing'] and self.channel is not None:
                await self.channel.trigger_typing()
            else:
                pass
        except IndexError:
            pass

    @background_loop.before_loop
    async def before_loop(self):
        """
        Wait until the bot is ready before starting the loop.
        """
        await self.bot.wait_until_ready()

    def cog_unload(self):
        """
        Stop the loop when the module is unloaded.
        """
        self.background_loop.cancel()

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.group(invoke_without_command=True)
    async def typing(self, ctx):
        """
        Function called by discord.py when the user invokes the typing command, which toggles typing.

        This function sets the channel object used by the background loop as well as sets the typing boolean in the
        database.

        Args:
            ctx (Context): Object provided by discord.py to allow for the context of the command to be interpreted.
        """
        if self.db.all()[0]['channel'] is not None:
            self.channel = discord.Client.get_channel(ctx.bot, int(self.db.all()[0]['channel']))
        else:
            self.channel = ctx.channel
        if self.channel is not None:
            boolean = self.db.all()[0]['send_typing']
            self.db.update({'send_typing': not boolean}, Query().send_typing == boolean)
            await ctx.send(f"Typing is now {str(not boolean)}")
        else:
            await ctx.send("Unable to start typing, channel not valid")

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @typing.command(name='channel')
    async def set_channel(self, ctx, *, channel: discord.TextChannel):
        """
        Function called by discord.py allowing the user to set a channel ID for the typing to occur in.

        This function validates (so far as int conversion) an ID and writes it to the database.

        Args:
            ctx (Context): Object provided by discord.py to allow for the context of the command to be interpreted.
            channel (discord.TextChannel): User input that is used to determine which channel to type in.
        """
        self.db.update({'channel': channel.id}, Query())
        await ctx.send(f"Set target channel ID to {channel.mention}")


def setup(bot):
    """
    Set up the bot.

    Args:
        bot (Bot): discord.py provided object that is used to assist with various discord interfacing
    """
    bot.add_cog(Typing(bot))
