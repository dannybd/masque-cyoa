""" Contains some fun commands that aren't that useful """
import discord
import re
from discord.ext import commands


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def fun_replies(self, message):
        if message.author == self.bot.user:
            return
        content = message.content.lower()
        channel = message.channel
        if re.match("50/50", content):
            await message.add_reaction("👀")
            await channel.send("roll up your sleeves!")
            return

    @commands.command(hidden=True, aliases=["hurray"])
    async def hooray(self, ctx):
        await ctx.send("🥳🎉🎊✨")


def setup(bot):
    cog = Example(bot)
    bot.add_cog(cog)
