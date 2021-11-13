""" Puts users into the experience to start """
from common import (
    get_cyoa_config,
    log_event,
    member_has_role,
    member_is_host,
)
import discord
from discord.ext import commands


class StartCYOA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def handle_messages(self, message):
        guild = message.guild
        if not guild:
            return
        cyoa = get_cyoa_config(guild)
        if not cyoa["start_phrase"] in message.content.lower():
            return
        actor = message.author
        if actor == self.bot.user:
            return
        if member_is_host(actor):
            return
        if (
            "channels_with_trapdoors" in cyoa
            and not message.channel.name in cyoa["channels_with_trapdoors"]
        ):
            return
        roles = [
            discord.utils.get(guild.roles, name=role) for role in cyoa["start_roles"]
        ]
        for role in roles:
            if member_has_role(actor, role.name):
                return
        await message.delete()
        await actor.add_roles(*roles)
        await log_event(
            guild=guild,
            actor=actor,
            title="Trapdoor activated!",
            description=message.content,
            channel=message.channel,
        )


def setup(bot):
    cog = StartCYOA(bot)
    bot.add_cog(cog)
