"""

YDITS for YQL

Copyright (C) 2024-2026 よね/Yone

https://github.com/YDITS/YDITS-YQL

"""

from __future__ import annotations

import discord
from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ydits_yql.client import Client


async def on_ready(
    self: Client,
    *,
    init_channels: Callable[[dict[str, discord.abc.Messageable]], None],
) -> None:
    print(f"[INFO ] {self.name} | {self.user} でログインしました。")
    channels: dict[str, discord.abc.Messageable] = {}
    channel = self.get_channel(self.channels_id["vxww50"])
    if not isinstance(channel, discord.abc.Messageable):
        print(
            f"[ERROR] {self.name} | vxww50 用に設定されたチャンネルを取得できません。"
        )
        return
    channels["vxww50"] = channel

    print(f"[LOG  ] {self.name} | 設定されたチャンネルIDの送信権限を検証しています...")

    for code, channel in channels.items():
        try:
            sent_message = await channel.send(
                "これは設定されたチャンネルIDの送信権限を検証するテストメッセージです。"
            )
            await sent_message.delete()

        except discord.errors.Forbidden:
            print(
                f"[ERROR] {self.name} | {code} 用に設定されたチャンネルID {self.channels_id[code]} への送信権限がありません。"
            )

        except Exception:
            print(
                f"[ERROR] {self.name} | {code} 用に設定されたチャンネルID {self.channels_id[code]} にメッセージを送信できません:\nチャンネルIDが正しいか、送信するサーバーにBOTが参加しているかを確認してください。"
            )

    print(
        f"[INFO ] {self.name} | 設定されたチャンネルIDの送信権限の検証が完了しました。"
    )

    init_channels(channels)
