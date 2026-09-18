import requests
from bs4 import BeautifulSoup

from ydits_yql.lib.jma_xml import JmaXml
from ydits_yql.lib.xml_parser import XmlParser
from ydits_yql.lib.jma_xml.vxww50 import Vxww50


def main():
    jma_xml = JmaXml()
    raw = jma_xml.get()

    xml_parser = XmlParser()
    xml_parser.parse(raw)
    entries = xml_parser.find_all("entry")

    on_updated_jma_xml(entries[0])


def on_updated_jma_xml(entry):
    if entry.title.string == "土砂災害警戒情報":
        response = requests.get(entry.link["href"])
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), "xml")
        data = Vxww50(soup)
        print(data.generate_formated_text())
        return


if __name__ == "__main__":
    main()
