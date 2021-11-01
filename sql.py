""" Methods for interacting with the SQL database """
import discord
import logging
import pymysql
from common import *


class SQL:
    @staticmethod
    def _get_db_connection(bot=None):
        if bot and bot.connection:
            bot.connection.ping(reconnect=True)
            return bot.connection

        logging.info("[SQL] No bot found, creating new connection")
        creds = config["db"]
        return pymysql.connect(
            host=creds["host"],
            port=creds.getint("port"),
            user=creds["user"].lower(),
            password=creds["passwd"],
            db=creds["db"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    @staticmethod
    def get_foo(channels, bot=None):
        connection = SQL._get_db_connection(bot=bot)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    *
                FROM foobar
                WHERE channel_id IN ({})
                """,
                tuple([c.id for c in channels]),
            )
            return {int(row["channel_id"]): row for row in cursor.fetchall()}
