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
                <id>https://www.data.jma.go.jp/developer/xml/data/20240829124010_0_VXWW50_220000.xml</id>
                <updated>2024-08-29T12:40:09Z</updated>
                <author>
                    <name>静岡県 静岡地方気象台</name>
                </author>
                <link type="application/xml" href="https://www.data.jma.go.jp/developer/xml/data/20240829124010_0_VXWW50_220000.xml"/>
                <content type="text">
                    【静岡県土砂災害警戒情報】＜概況＞ 降り続く大雨のため、土砂災害警戒区域等では命に危険が及ぶ土砂災害がいつ発生してもおかしくない非常に危険な状況です。 ＜とるべき措置＞ 避難が必要となる危険な状況となっています【警戒レベル４相当情報［土砂災害］】 崖の近くや谷の出口など土砂災害警戒区域等にお住まいの方は、市町から発令される避難指示などの情報に留意し、少しでも安全な場所への速やかな避難を心がけてください。
                </content>
            </entry>
            """
