import os
import logging
import ydits_yql


if __name__ == "__main__":
    os.system("clear")

    log_handler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w"
    )

    my_bot = ydits_yql.Bot(
        token=ydits_yql.config.DISCORD_BOT["token"],
        log_handler=log_handler,
        channels_id=ydits_yql.config.DISCORD_BOT["channels"],
    )
