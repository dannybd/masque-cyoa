import configparser
import discord
import json
import logging
import traceback

from discord.ext import commands
from functools import lru_cache
from hashlib import md5


GUILDS = {
    "test": 432741711786278913,
    "prod": 894375696141529129,
}


def get_guild_key(guild):
    inv_guilds = {v: k for k, v in GUILDS.items()}
    return inv_guilds.get(guild.id)


def member_has_role(member, role_name):
    return bool(discord.utils.get(member.roles, name=role_name))


def member_is_host(member):
    guild = member.guild
    cyoa = get_cyoa_config(member.guild)
    return member_has_role(member, cyoa["host_role"])


CACHE_BUSTER = 0


def bust_cache(guild):
    global CACHE_BUSTER
    CACHE_BUSTER += 1
    get_cyoa_config(guild)
    return CACHE_BUSTER


def get_cyoa_config(guild):
    global CACHE_BUSTER
    while True:
        try:
            return get_cyoa_config_impl(guild, CACHE_BUSTER)
        except Exception as e:
            if CACHE_BUSTER == 0:
                raise e
            exc = "{}: {}".format(type(e).__name__, traceback.format_exc())
            logging.warning("Failed to read CYOA config\n{}".format(exc))
            CACHE_BUSTER -= 1


@lru_cache(maxsize=128)
def get_cyoa_config_impl(guild, cache_counter):
    key = get_guild_key(guild)
    logging.info(
        "Reloading data for GUILD {}, cache counter = {}".format(
            key.upper(), cache_counter
        )
    )
    with open("data/{}.json".format(key), "r") as f:
        return json.load(f)


def get_stable_embed_color(msg):
    hash = md5(msg.encode("utf-8")).hexdigest()
    hue = int(hash, 16) / 16 ** len(hash)
    return discord.Color.from_hsv(hue, 0.655, 1)


async def log_event(guild, actor, title, description=None, channel=None):
    logging.info(
        '>>> GUILD {}: "{}" by {}'.format(
            get_guild_key(guild).upper(),
            title,
            str(actor),
        )
    )
    cyoa = get_cyoa_config(guild)
    if not "logging_channel" in cyoa:
        return
    logging_channel = discord.utils.get(guild.channels, name=cyoa["logging_channel"])
    if not logging_channel:
        return
    embed = discord.Embed(
        color=get_stable_embed_color(title),
        title=title,
        description=description,
    )
    embed.add_field(name="Who?", value=actor.mention, inline=True)
    if channel:
        embed.add_field(name="Channel", value=channel.mention, inline=True)
    await logging_channel.send(embed=embed)


config = configparser.ConfigParser()
config.read("config.ini")
