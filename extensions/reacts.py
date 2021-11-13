""" Auto-delete non-host message in the channels """
from common import get_guild_key, member_has_role, member_is_host, get_cyoa_config
import discord
from discord.ext import commands
from emoji import emojize


class Reacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_raw_reaction_add")
    async def handle_reacts(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        if not payload.guild_id:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        channel = guild.get_channel(payload.channel_id)
        if not channel:
            return
        message = await channel.fetch_message(payload.message_id)
        if not message:
            return
        if message.author != self.bot.user:
            return
        cyoa = get_cyoa_config(guild)
        if channel.name not in cyoa["channels"]:
            return
        channel_cyoa = cyoa["channels"][channel.name]
        emoji = str(payload.emoji)
        if emoji is None:
            return
        button = next(
            (button for button in channel_cyoa["buttons"] if button["emoji"] == emoji),
            None,
        )
        if not button:
            return
        actor = payload.member
        await actor.remove_roles(
            discord.utils.get(guild.roles, name=channel_cyoa["role"])
        )
        await message.remove_reaction(emoji, actor)
        destination_channel_cyoa = cyoa["channels"].get(button.get("channel"))
        if destination_channel_cyoa:
            await actor.add_roles(
                discord.utils.get(guild.roles, name=destination_channel_cyoa["role"])
            )
        else:
            # We've escaped! Remove the roles
            start_roles = [
                discord.utils.get(guild.roles, name=role) for role in cyoa["start_roles"]
            ]
            await actor.remove_roles(*roles)
        if "dm" in button:
            await actor.send(button["dm"])


def setup(bot):
    cog = Reacts(bot)
    bot.add_cog(cog)
