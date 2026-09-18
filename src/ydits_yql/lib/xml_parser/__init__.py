"""

YDITS for YQL

Copyright (C) 2024-2026 よね/Yone

https://github.com/YDITS/YDITS-YQL

"""

import bs4
from bs4 import BeautifulSoup
from bs4.element import PageElement
from typing import Any


class XmlParser:
    def __init__(self) -> None:
        self.name = "XmlParser"
        self.soup: BeautifulSoup | None = None

    def parse(self, xml_raw: Any) -> None:
        try:
            self.soup = BeautifulSoup(xml_raw, "xml")
        except bs4.FeatureNotFound as _:
            print(
                f"[ERROR] {self.name} | 必要なパッケージがインストールされていません。\n以下のコマンドを使用してXMLパーサーをインストールしてください:\n    pip install lxml"
            )

    def find_all(self, name: str) -> list[PageElement]:
        if self.soup is None:
            return []
        return list(self.soup.find_all(name))
