import configparser
import discord
from discord.ext import commands
from functools import lru_cache
import json
from hashlib import md5


GUILDS = {
    "test": 432741711786278913,
    "prod": 894375696141529129,
}


def get_guild_key(guild):
    inv_guilds = {v: k for k, v in GUILDS.items()}
    return inv_guilds.get(guild.id)


def is_in_guilds(*guild_keys):
    """Only allow this command on certain guilds"""

    async def predicate(ctx):
        return get_guild_key(ctx.guild) in guild_keys

    return commands.check(predicate)


def member_has_role(member, role_name):
    return bool(discord.utils.get(member.roles, name=role_name))


def member_is_host(member):
    guild = member.guild
    cyoa = get_cyoa_config(member.guild)
    return member_has_role(member, cyoa["host_role"])


@lru_cache(maxsize=128)
def get_cyoa_config(guild):
    with open("data/{}.json".format(get_guild_key(guild)), "r") as f:
        return json.load(f)


def get_stable_embed_color(msg):
    hash = md5(msg.encode("utf-8")).hexdigest()
    hue = int(hash, 16) / 16 ** len(hash)
    return discord.Color.from_hsv(hue, 0.655, 1)


config = configparser.ConfigParser()
config.read("config.ini")
