from bs4 import BeautifulSoup


class XmlParser:
    def parse(self, xml_raw):
        self.soup = BeautifulSoup(xml_raw, "xml")

    def find_all(self, name):
        return self.soup.find_all(name)
