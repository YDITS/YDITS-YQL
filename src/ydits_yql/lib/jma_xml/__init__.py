import requests


class JmaXml:
    def __init__(self) -> None:
        self.uri = "https://www.data.jma.go.jp/developer/xml/feed/extra.xml"
        self.latest_id = None
        self.last_id = None

    def get(self):
        response = requests.get(self.uri)
        response.encoding = response.apparent_encoding
        return response.content
        # return self.debug_entry()  # DEBUG

    def debug_entry(self):
        return """
            <entry>
                <title>土砂災害警戒情報</title>
                <id>https://www.data.jma.go.jp/developer/xml/data/20240921044030_0_VXWW50_050000.xml</id>
                <updated>2024-09-21T04:40:29Z</updated>
                <author>
                    <name>秋田県 秋田地方気象台</name>
                </author>
                <link type="application/xml" href="https://www.data.jma.go.jp/developer/xml/data/20240921044030_0_VXWW50_050000.xml"/>
                <content type="text">【秋田県土砂災害警戒情報】＜概況＞ 大雨のため、警戒対象地域では土砂災害の危険度が高まっています。 ＜とるべき措置＞ 避難が必要となる危険な状況となっています【警戒レベル４相当情報［土砂災害］】。 崖の近くや谷の出口など土砂災害警戒区域等にお住まいの方は、市町村から発令される避難指示などの情報に留意し、少しでも安全な場所への速やかな避難を心がけてください。</content>
            </entry>
            """
