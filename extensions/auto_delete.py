""" Auto-delete non-host message in the channels """
from common import get_guild_key, member_has_role, member_is_host, get_cyoa_config
import discord
from discord.ext import commands
from emoji import emojize


class AutoDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def handle_messages(self, message):
        cyoa = get_cyoa_config(message.guild)
        if message.channel.name not in cyoa["channels"]:
            return
        actor = message.author
        if actor == self.bot.user:
            return
        if member_is_host(actor):
            return
        await message.delete()


def setup(bot):
    cog = AutoDelete(bot)
    bot.add_cog(cog)
