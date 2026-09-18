"""

YDITS for YQL

Copyright (C) 2024-2026 よね/Yone

https://github.com/YDITS/YDITS-YQL

"""

from typing import TypedDict


class DiscordBotConfig(TypedDict):
    token: str
    channels: dict[str, int]


DISCORD_BOT: DiscordBotConfig = {
    "token": "",
    "channels": {
        "vxww50": 0000000000000000000,
    },
}
