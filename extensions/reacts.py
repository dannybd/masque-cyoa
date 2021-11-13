""" Auto-delete non-host message in the channels """
import discord

from common import get_cyoa_config, log_event
from discord.ext import commands


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
        await message.remove_reaction(emoji, actor)
        if "role" in channel_cyoa:
            await actor.remove_roles(
                discord.utils.get(guild.roles, name=channel_cyoa["role"])
            )
        destination_channel_cyoa = cyoa["channels"].get(button.get("channel"))
        if destination_channel_cyoa:
            await actor.add_roles(
                discord.utils.get(guild.roles, name=destination_channel_cyoa["role"])
            )
        else:
            # We've escaped! Remove all CYOA roles
            cyoa_roles = [
                role
                for role in guild.roles
                if role.name
                in [c["role"] for c in cyoa["channels"].values() if "role" in c]
            ]
            await actor.remove_roles(
                # Start with removing mute role, so everything reappears immediately
                discord.utils.get(guild.roles, name=cyoa["mute_role"]),
                *cyoa_roles,
            )
            await log_event(
                guild=guild,
                actor=actor,
                title="Guest exited the catacombs.",
                channel=channel,
            )
        dm_cyoa = cyoa["dms"].get(button.get("dm"))
        if dm_cyoa:
            if "role" in dm_cyoa:
                await actor.add_roles(
                    discord.utils.get(guild.roles, name=dm_cyoa["role"])
                )
            await actor.send(dm_cyoa["content"])
            await log_event(
                guild=guild,
                actor=actor,
                title="Guest reached {}!".format(button["dm"]),
                channel=channel,
            )


def setup(bot):
    cog = Reacts(bot)
    bot.add_cog(cog)
