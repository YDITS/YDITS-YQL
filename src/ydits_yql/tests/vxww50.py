"""

YDITS for YQL

Copyright (C) 2024-2026 よね/Yone

https://github.com/YDITS/YDITS-YQL

"""

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from ydits_yql.lib.jma_xml import JmaXml
from ydits_yql.lib.xml_parser import XmlParser
from ydits_yql.lib.jma_xml.vxww50 import Vxww50


def main() -> None:
    jma_xml = JmaXml()
    raw = jma_xml.get()

    xml_parser = XmlParser()
    xml_parser.parse(raw)
    entries = xml_parser.find_all("entry")

    if isinstance(entries[0], Tag):
        on_updated_jma_xml(entries[0])


def on_updated_jma_xml(entry: Tag) -> None:
    title = entry.find("title")
    link = entry.find("link")
    href = link.get("href") if isinstance(link, Tag) else None
    if (
        isinstance(title, Tag)
        and title.string == "土砂災害警戒情報"
        and isinstance(href, str)
    ):
        response = requests.get(href)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), "xml")
        data = Vxww50(soup)
        print(data.generate_formated_text())
        return


if __name__ == "__main__":
    main()
