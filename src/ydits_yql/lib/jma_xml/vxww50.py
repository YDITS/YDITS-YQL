"""

YDITS for YQL

Copyright (C) 2024-2026 よね/Yone

https://github.com/YDITS/YDITS-YQL

"""

import re
from bs4.element import Tag
from datetime import datetime
from ydits_yql.lib.discord_embed import DiscordEmbed


def _required_tag(parent: Tag, name: str) -> Tag:
    element = parent.find(name)
    if not isinstance(element, Tag):
        raise ValueError(f"Missing XML element: {name}")
    return element


def _required_text(parent: Tag, name: str) -> str:
    element = _required_tag(parent, name)
    if element.string is None:
        raise ValueError(f"Missing XML text: {name}")
    return element.string


class Vxww50:
    """
    気象庁防災情報XML | VXWW50/土砂災害警戒情報

    仕様書にあたっては https://dmdata.jp/docs/jma/manual/0271-0271.pdf を参照すること。
    """

    def __init__(self, data: Tag) -> None:
        self.time_data_format = "%Y-%m-%dT%H:%M:%S+09:00"
        self.time_export_format = "%Y年%m月%d日 %H時%M分"

        try:
            self.title = _required_text(data, "Title")
            self.status = _required_text(data, "Status")
            self.publishing_office = _required_text(data, "PublishingOffice")
            report_time = _required_text(data, "ReportDateTime")
            self.info_type = _required_text(data, "InfoType")
            self.text = _required_text(data, "Text")

            headline = _required_tag(data, "Headline")
            information = _required_tag(headline, "Information")
            item = _required_tag(information, "Item")
            self.name = _required_text(_required_tag(item, "Kind"), "Name")
            areas = _required_tag(item, "Areas")
            self.areas: list[Tag] = list(areas.find_all("Area"))

            self.report_time = datetime.strptime(report_time, self.time_data_format)
            self.report_time = self.report_time.strftime(self.time_export_format)

            self.text = re.sub(r"＜(.*?)＞", r"【\1】", self.text, count=1)
            self.text = re.sub(r"＜(.*?)＞", r"\n【\1】", self.text)

        except Exception as error:
            print(f"[ERROR] Parse VXWW50 has failed: {error}")

    def generate_formated_text(self) -> str:
        areas = ""

        for area in self.areas:
            areas += f"{_required_text(area, 'Name')}　"

        return (
            f"{self.title}\n"
            f"{self.report_time}\n"
            f"{self.publishing_office} {self.info_type}\n\n"
            f"{self.text}\n\n"
            f"- {self.name}\n"
            f"    {areas}"
        )

    def generate_formated_discord_embed(self) -> DiscordEmbed:
        areas = ""
        for area in self.areas:
            areas += f"## ・{_required_text(area, 'Name')}\n"

        if self.name == "警戒":
            colour = 0xFF4040
        elif self.name == "解除":
            colour = 0x404040
        else:
            colour = 0x404040

        return DiscordEmbed(
            title=self.title,
            description=(
                f"{self.report_time}\n"
                f"{self.publishing_office} {self.info_type}\n\n"
                f"{self.text}\n\n"
                f"＜発表地域はこちら＞\n"
                f"{areas}"
            ),
            colour=colour,
        )
