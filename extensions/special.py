""" Auto-delete non-host message in the channels """
import discord
import re

from common import get_cyoa_config, log_event, member_is_host
from discord.ext import commands


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
                    discord.utils.get(guild.roles, name="fx box"),
                    discord.utils.get(guild.roles, name="atrium"),
                )
                await actor.remove_roles(
                    discord.utils.get(guild.roles, name="south tunnels"),
                )
                await log_event(
                    guild=guild,
                    actor=actor,
                    title="Atrium found!",
                )


def setup(bot):
    cog = Special(bot)
    bot.add_cog(cog)
