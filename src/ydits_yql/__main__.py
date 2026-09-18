import logging
import ydits_yql
from ydits_yql import config
from ydits_yql.bot import Bot

def main() -> None:
    print(f"{ydits_yql.__title__} を起動しています...")

    log_handler = logging.FileHandler(
        filename="discord.log",
        encoding="utf-8",
        mode="w",
    )

    my_bot = Bot(
        token=config.DISCORD_BOT["token"],
        log_handler=log_handler,
        channels_id=config.DISCORD_BOT["channels"],
    )

if __name__ == "__main__":
    main()
