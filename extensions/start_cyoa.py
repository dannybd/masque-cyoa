""" Puts users into the experience to start """
from common import get_guild_key, member_has_role, member_is_host, get_cyoa_config
import discord
from discord.ext import commands
from emoji import emojize


class StartCYOA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def handle_messages(self, message):
        guild = message.guild
        cyoa = get_cyoa_config(guild)
        if not cyoa["start_phrase"] in message.content.lower():
            return
        actor = message.author
        if actor == self.bot.user:
            return
        if member_is_host(actor):
            return
        roles = [
            discord.utils.get(guild.roles, name=role) for role in cyoa["start_roles"]
        ]
        for role in roles:
            if member_has_role(actor, role.name):
                return
        await actor.add_roles(*roles)


def setup(bot):
    cog = StartCYOA(bot)
    bot.add_cog(cog)
