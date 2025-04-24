import logging
import xml.etree.ElementTree as ET

import bedrock
import jmespath
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def cleaned_html(html_json):
    """HTML整形処理をする

    Args:
        html_json (json): 整形するHTMLのjson

    Returns:
        str: 整形後のHTML
    """

    logger.info("HTML整形処理開始")
    urls = jmespath.search("web.results[*].url", html_json)
    cleaned_htmls = []
    for url in urls:
        logger.info(f"HTML整形先URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = "utf-8"

        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup.find_all(["script", "style"]):
            tag.decompose()
        cleaned_html = soup.get_text(separator="\n", strip=True)
        cleaned_htmls.append(cleaned_html)

    logger.info("HTML整形処理完了")
    return "\n".join(cleaned_htmls)


def parse_google_news(xml_str: str):
    """Google ニュース XML整形処理する

    Args:
        xml_str (str): 整形するXMLの文字列

    Returns:
        str: 整形後のニュース情報
    """

    logger.info("XML整形処理開始")
    root = ET.fromstring(xml_str)
    channel = root.find("channel")
    items = channel.findall("item")[:1]
    news_list = []
    for item in items:
        title = item.findtext("title")
        description = BeautifulSoup(
            item.findtext("description"), "html.parser"
        ).get_text()
        pub_date = item.findtext("pubDate")
        source = item.findtext("source")

        news_text = f"タイトル: {title}\n概要: {description}\n公開日: {pub_date}\n参考元: {source}"
        news_list.append(news_text)

    logger.info("XML整形処理完了")
    return "\n".join(news_list)
