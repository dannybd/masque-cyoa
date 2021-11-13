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
        content = channel_cyoa["content"]
        buttons = channel_cyoa["buttons"]
        if buttons:
            content += "\n"
        for button in buttons:
            content += "\n{emoji}  {desc}".format(**button)
        message = await channel.send(content)
        for button in buttons:
            await message.add_reaction(button["emoji"])
        await ctx.message.delete()


def setup(bot):
    cog = SetupCYOA(bot)
    bot.add_cog(cog)
