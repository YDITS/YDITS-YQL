import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup

from ydits_yql.on_ready import on_ready
from ydits_yql.on_message import on_message
from ydits_yql.lib.jma_xml import JmaXml
from ydits_yql.lib.xml_parser import XmlParser
from ydits_yql.lib.jma_xml.vxww50 import Vxww50


class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        self.name = "Client"
        print(f"[LOG  ] {self.name} | イニシャライズしています...")

        super().__init__(*args, **kwargs)

        self.channels = {}
        self.channels_id = kwargs["channels_id"]

        self.jma_xml = JmaXml()
        self.xml_parser = XmlParser()

        self.jma_request_interval = 60
        self.jma_request_count = -1

    async def on_connect(self):
        print(f"[INFO ] {self.name} | Discord APIに接続しました。")

    async def on_disconnect(self):
        print(f"[INFO ] {self.name} | Discord APIから切断されました。")

    async def on_ready(self):
        def init_channels(channels):
            self.channels = channels

        await on_ready(self, init_channels=init_channels)

        print(f"[LOG  ] {self.name} | タスクを開始しています...")
        self.tasks.start()

    async def on_message(self, message):
        on_message(self, message=message)

    async def setup_hook(self) -> None:
        print(f"[LOG  ] {self.name} | フックをセットアップしています...")

    @tasks.loop(seconds=1)
    async def tasks(self):
        if self.jma_request_count >= self.jma_request_interval or self.jma_request_count == -1:
            await self.jma_xml_task()
        self.jma_request_count += 1

    async def jma_xml_task(self):
        self.jma_request_count = 0

        raw = self.jma_xml.get()
        self.xml_parser.parse(raw)
        entries = self.xml_parser.find_all("entry")

        self.jma_xml.latest_id = entries[0].id.string

        if (
            self.jma_xml.latest_id != self.jma_xml.last_id
            and self.jma_xml.last_id != None
        ):
            await self.on_updated_jma_xml(entries[0])
            self.jma_xml.last_id = self.jma_xml.latest_id
            return

        self.jma_xml.last_id = self.jma_xml.latest_id

    async def on_updated_jma_xml(self, entry):
        print(f"[LOG  ] {self.name} | JMA XMLが更新されました: {entry.title.string}")

        if entry.title.string == "土砂災害警戒情報":
            response = requests.get(entry.link["href"])
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
