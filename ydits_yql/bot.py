import logging
import discord
import ydits_yql
from ydits_yql.client import Client
from ydits_yql.lib.clear_console import clear_console


class Bot:
    def __init__(self, *, token, log_handler, channels_id) -> None:
        self.name = "Bot"

        print(f"[LOG  ] {self.name}    | イニシャライズしています...")

        self.show_logo()
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = Client(intents=intents, channels_id=channels_id)
        self.run(token, log_handler)

    def show_logo(self):
        clear_console("clear")

        print(
            f"{ydits_yql.__title__} Ver {ydits_yql.__version__}\n"
            f"{ydits_yql.__copyright__}\n\n"
            f"discord.py v{discord.__version__}\n\n" + "-" * 20 + "\n"
        )

    def run(self, token, log_handler):
        print(f"[LOG  ] {self.name}    | トークンを検証しています...")

        if not (token):
            print(f"[ERROR] {self.name}    | トークンが指定されていません。")
            raise ValueError("Improper token has been passed.")

        print(f"[LOG  ] {self.name}    | Discord APIに接続しています...")

        try:
            self.client.run(
                token=token, log_handler=log_handler, log_level=logging.DEBUG
            )

        except discord.errors.LoginFailure as error:
            print(
                f"[ERROR] {self.name}    | Discord APIにログインできませんでした。トークンが正しいか確認してください。"
            )
            raise discord.errors.LoginFailure(error)
