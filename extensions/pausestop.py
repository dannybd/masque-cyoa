""" Alerts mods when pause and stop reacts are used """
from common import get_guild_key
import discord
from discord.ext import commands
from emoji import emojize

CARETAKER_ROLES = {
    'sibr': 738108360964178082,
    'dannybd-test': 904974590986559508,
}

def caretaker_role(guild):
    role_id = CARETAKER_ROLES[get_guild_key(guild)]
    return guild.get_role(role_id)

EMOJIS = [emojize(":pause_button:"), emojize(":stop_sign:")]

class PauseStop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_raw_reaction_add")
    async def handle_reacts(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        if not payload.guild_id:
            return
        emoji = str(payload.emoji)
        if emoji is None:
            return
        if emoji not in EMOJIS:
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
        if any(emoji in message.content for emoji in EMOJIS):
            # Ran already on the content
            return
        reaction_count = sum(
            reaction.count
            for reaction in message.reactions
            if str(reaction.emoji) == emoji
        )
        if reaction_count != 1:
            # Not the first one of these
            return
        actor = payload.member
        if caretaker_role(guild).id in [role.id for role in actor.roles]:
            return
        report_channel = guild.get_channel(904863674806718506)
        await report_channel.send(
            ("**Heads up {}:** {} posted in {} by {}: \n" + "{}").format(
                caretaker_role(guild).mention,
                emoji,
                channel.mention,
                actor.mention,
                message.jump_url,
            )
        )

    @commands.Cog.listener("on_message")
    async def handle_messages(self, message):
        emoji = next((emoji for emoji in EMOJIS if emoji in message.content), None)
        if not emoji:
            return
        actor = message.author
        if actor == self.bot.user:
            return
        guild = message.guild
        if caretaker_role(guild).id in [role.id for role in actor.roles]:
            return
        report_channel = guild.get_channel(904863674806718506)
        await report_channel.send(
            ("**Heads up {}:** {} posted in {} by {}: \n" + "{}").format(
                caretaker_role(guild).mention,
                emoji,
                message.channel.mention,
                actor.mention,
                message.jump_url,
            )
        )


def setup(bot):
    cog = PauseStop(bot)
    bot.add_cog(cog)
