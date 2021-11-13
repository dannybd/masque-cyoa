""" Auto-delete non-host message in the channels """
import discord

from common import get_cyoa_config, member_is_host
from discord.ext import commands


class AutoDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def handle_messages(self, message):
        if not message.guild:
            return
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
