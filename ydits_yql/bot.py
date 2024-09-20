import logging
import discord
import ydits_yql
from ydits_yql.client import Client


class Bot:
    def __init__(self, *, token, log_handler, channels_id) -> None:
        self.show_logo()
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = Client(intents=intents, channels_id=channels_id)
        self.login(token, log_handler)

    def show_logo(self):
        print(
            f"{ydits_yql.__title__} Ver {ydits_yql.__version__}\n"
            f"{ydits_yql.__copyright__}\n\n"
            f"discord.py v{discord.__version__}\n\n" + "-" * 20 + "\n"
        )

    def login(self, token, log_handler):
        if not (token):
            raise ValueError("Improper token has been passed.")

        try:
            self.client.run(
                token=token, log_handler=log_handler, log_level=logging.DEBUG
            )

        except discord.errors.LoginFailure as error:
            raise discord.errors.LoginFailure(error)
