import re
from bs4 import BeautifulSoup
from datetime import datetime
from ydits_yql.lib.discord_embed import DiscordEmbed


class Vxww50:
    """
    気象庁防災情報XML | VXWW50/土砂災害警戒情報

    仕様書にあたっては https://dmdata.jp/docs/jma/manual/0271-0271.pdf を参照すること。
    """

    def __init__(self, data):
        self.time_data_format = "%Y-%m-%dT%H:%M:%S+09:00"
        self.time_export_format = "%Y年%m月%d日 %H時%M分"

        try:
            self.title = data.find("Title").string
            self.status = data.find("Status").string
            self.publishing_office = data.find("PublishingOffice").string
            self.report_time = data.find("ReportDateTime").string
            self.info_type = data.find("InfoType").string
            self.text = data.find("Text").string
            self.name = data.find("Headline").Information.Item.Kind.Name.string
            self.areas = data.find("Headline").Information.Item.Areas.find_all("Area")

            self.report_time = datetime.strptime(
                self.report_time, self.time_data_format
            )
            self.report_time = self.report_time.strftime(self.time_export_format)

            self.text = re.sub(r"＜(.*?)＞", r"【\1】", self.text, count=1)
            self.text = re.sub(r"＜(.*?)＞", r"\n【\1】", self.text)

        except Exception as error:
            print(f"[ERROR] Parse VXWW50 has failed: {error}")

    def generate_formated_text(self):
        areas = ""

        for area in self.areas:
            areas += f"{area.find('Name').string}　"

        return (
            f"{self.title}\n"
            f"{self.report_time}\n"
            f"{self.publishing_office} {self.info_type}\n\n"
            f"{self.text}\n\n"
            f"- {self.name}\n"
            f"    {areas}"
        )

    def generate_formated_discord_embed(self):
        areas = ""
        for area in self.areas:
            areas += f"## ・{area.find('Name').string}\n"

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
