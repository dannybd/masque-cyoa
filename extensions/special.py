""" Auto-delete non-host message in the channels """
from common import get_guild_key, member_has_role, member_is_host, get_cyoa_config
import discord
from discord.ext import commands
import re


class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def handle_messages(self, message):
        guild = message.guild
        if not guild:
            return
        cyoa = get_cyoa_config(guild)
        if message.channel.name not in cyoa["channels"]:
            return
        actor = message.author
        if actor == self.bot.user:
            return
        if member_is_host(actor):
            return
        content = message.content.lower()
        if message.channel.name == "south-tunnels":
            pattern = re.compile("press|touch|push|button|click")
            if pattern.match(content):
                await actor.add_roles(
                    # discord.utils.get(guild.roles, name="fxbox"),
                    discord.utils.get(guild.roles, name="atrium"),
                )
                await actor.remove_roles(
                    discord.utils.get(guild.roles, name="south tunnels"),
                )


def setup(bot):
    cog = Special(bot)
    bot.add_cog(cog)
