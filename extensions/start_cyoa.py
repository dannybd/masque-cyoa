""" Puts users into the experience to start """
from common import (
    get_cyoa_config,
    get_guild_key,
    get_stable_embed_color,
    member_has_role,
    member_is_host,
)
import discord
from discord.ext import commands
from emoji import emojize


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
        roles = [
            discord.utils.get(guild.roles, name=role) for role in cyoa["start_roles"]
        ]
        for role in roles:
            if member_has_role(actor, role.name):
                return
        await message.delete()
        await actor.add_roles(*roles)
        start_message_dump_channel = discord.utils.get(
            guild.channels,
            name=cyoa.get("start_message_dump_channel"),
        )
        if start_message_dump_channel:
            embed = discord.Embed(
                color=get_stable_embed_color(str(message.channel)),
                title="Trapdoor activated!",
                description=message.content,
            )
            embed.add_field(name="Channel", value=message.channel.mention, inline=True)
            embed.add_field(name="Who?", value=actor.mention, inline=True)
            await start_message_dump_channel.send(embed=embed)


def setup(bot):
    cog = StartCYOA(bot)
    bot.add_cog(cog)
