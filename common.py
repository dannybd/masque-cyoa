import configparser
from discord.ext import commands


GUILDS = {
    "dannybd-test": 432741711786278913,
}


def get_guild_key(guild):
    inv_guilds = {v: k for k, v in GUILDS.items()}
    return inv_guilds.get(guild.id)


def is_in_guilds(*guild_keys):
    """Only allow this command on certain guilds"""

    async def predicate(ctx):
        return get_guild_key(ctx.guild) in guild_keys

    return commands.check(predicate)


config = configparser.ConfigParser()
config.read("config.ini")
