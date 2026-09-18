"""

YDITS for YQL

Copyright (C) 2024-2026 よね/Yone

https://github.com/YDITS/YDITS-YQL

"""

from __future__ import annotations

import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Any

from ydits_yql.on_ready import on_ready
from ydits_yql.on_message import on_message
from ydits_yql.lib.jma_xml import JmaXml
from ydits_yql.lib.xml_parser import XmlParser
from ydits_yql.lib.jma_xml.vxww50 import Vxww50


class Client(discord.Client):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.name = "Client"
        print(f"[LOG  ] {self.name} | イニシャライズしています...")

        super().__init__(*args, **kwargs)

        self.channels: dict[str, discord.abc.Messageable] = {}
        self.channels_id = kwargs["channels_id"]

        self.jma_xml = JmaXml()
        self.xml_parser = XmlParser()

        self.jma_request_interval: int = 60
        self.jma_request_count = -1

    async def on_connect(self) -> None:
        print(f"[INFO ] {self.name} | Discord APIに接続しました。")

    async def on_disconnect(self) -> None:
        print(f"[INFO ] {self.name} | Discord APIから切断されました。")

    async def on_ready(self):
        def init_channels(channels: dict[str, discord.abc.Messageable]) -> None:
            self.channels = channels

        await on_ready(self, init_channels=init_channels)

        print(f"[LOG  ] {self.name} | タスクを開始しています...")
        self.tasks.start()

    async def on_message(self, message: discord.Message):
        on_message(self, message=message)

    async def setup_hook(self) -> None:
        print(f"[LOG  ] {self.name} | フックをセットアップしています...")

    @tasks.loop(seconds=1)
    async def tasks(self):
        if (
            self.jma_request_count >= self.jma_request_interval
            or self.jma_request_count == -1
        ):
            await self.jma_xml_task()
        self.jma_request_count += 1

    async def jma_xml_task(self):
        self.jma_request_count = 0

        raw = self.jma_xml.get()
        self.xml_parser.parse(raw)
        entries = self.xml_parser.find_all("entry")
        if not entries or not isinstance(entries[0], Tag):
            return

        entry = entries[0]
        entry_id = entry.find("id")
        if not isinstance(entry_id, Tag) or entry_id.string is None:
            return

        self.jma_xml.latest_id = entry_id.string

        if (
            self.jma_xml.latest_id != self.jma_xml.last_id
            and self.jma_xml.last_id != None
        ):
            await self.on_updated_jma_xml(entry)
            self.jma_xml.last_id = self.jma_xml.latest_id
            return

        self.jma_xml.last_id = self.jma_xml.latest_id

    async def on_updated_jma_xml(self, entry: Tag) -> None:
        title = entry.find("title")
        if not isinstance(title, Tag) or title.string is None:
            return

        print(f"[LOG  ] {self.name} | JMA XMLが更新されました: {title.string}")

        if title.string == "土砂災害警戒情報":
            link = entry.find("link")
            href = link.get("href") if isinstance(link, Tag) else None
            if not isinstance(href, str):
                return

            response = requests.get(href)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), "xml")
            data = Vxww50(soup)
            await self.channels["vxww50"].send(
                embed=data.generate_formated_discord_embed()
            )
            return

    @tasks.before_loop
    async def before_task(self):
        print(f"[LOG  ] {self.name} | ログインを待っています...")
        await self.wait_until_ready()
