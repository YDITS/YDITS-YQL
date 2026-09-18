"""

YDITS for YQL

Copyright (C) 2024-2026 よね/Yone

https://github.com/YDITS/YDITS-YQL

"""

from __future__ import annotations

import discord
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ydits_yql.client import Client


def on_message(self: Client, *, message: discord.Message) -> None:
    if is_me(self, message=message):
        return

    if is_bot(message=message):
        return


def is_me(self: Client, *, message: discord.Message) -> bool:
    return message.author == self.user


def is_bot(*, message: discord.Message) -> bool:
    return message.author.bot
