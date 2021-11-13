""" Setup each channel correctly at its start """
from common import get_guild_key, member_has_role, member_is_host, get_cyoa_config
import discord
from discord.ext import commands
from emoji import emojize


class SetupCYOA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def setup(self, ctx):
        if not member_is_host(ctx.author):
            return
        if ctx.author.bot:
            return
        cyoa = get_cyoa_config(ctx.guild)
        channels = cyoa["channels"]
        channel = ctx.channel
        if channel.name not in cyoa["channels"]:
            return
        channel_cyoa = cyoa["channels"][channel.name]
        await channel.purge()
        await channel.edit(sync_permissions=True)
        if "role" in channel_cyoa:
            await channel.set_permissions(
                discord.utils.get(ctx.guild.roles, name=channel_cyoa["role"]),
                read_messages=True,
                send_messages=True,
            )
        content = channel_cyoa["content"]
        buttons = channel_cyoa["buttons"]
        if buttons:
            content += "\n"
        for button in buttons:
            content += "\n{emoji}  {desc}".format(**button)
        message = await channel.send(content)
        for button in buttons:
            await message.add_reaction(button["emoji"])


def setup(bot):
    cog = SetupCYOA(bot)
    bot.add_cog(cog)
