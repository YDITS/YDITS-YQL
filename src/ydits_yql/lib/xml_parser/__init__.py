import bs4
from bs4 import BeautifulSoup


class XmlParser:
    def __init__(self):
        self.name = "XmlParser"

    def parse(self, xml_raw):
        try:
            self.soup = BeautifulSoup(xml_raw, "xml")
        except bs4.FeatureNotFound as e:
            print(f"[ERROR] {self.name} | 必要なパッケージがインストールされていません。\n以下のコマンドを使用してXMLパーサーをインストールしてください:\n    pip install lxml")

    def find_all(self, name):
        return self.soup.find_all(name)
