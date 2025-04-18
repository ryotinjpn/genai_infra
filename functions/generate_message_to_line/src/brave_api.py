import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def cleaned_html(html_json):
    """HTML整形処理をする

    Args:
        html_json (json): 整形するHTMLのjson

    Returns:
        list: 整形後のHTML
    """

    cleaned_htmls = []
    logger.info("HTML整形処理開始")
    for item in html_json.get("web", {}).get("results", []):
        response = requests.get(item.get("url"))
        response.raise_for_status()

        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, "html.parser")

        # bodyタグを取得
        body_tag = soup.body

        if body_tag:
            body_soup = BeautifulSoup(str(body_tag), "html.parser")

            for tag in body_soup.find_all(
                [
                    "script",
                    "style",
                    "nav",
                    "header",
                    "footer",
                    "aside",
                    "noscript",
                    "iframe",
                    "img",
                ]
            ):
                tag.decompose()

            unwanted_classes = [
                "ads",
                "ad-",
                "banner",
                "menu",
                "nav",
                "sidebar",
                "footer",
                "comments",
                "related",
            ]
            for class_name in unwanted_classes:
                for tag in body_soup.find_all(
                    class_=lambda x: x and class_name in x.lower()
                ):
                    tag.decompose()

            unwanted_ids = [
                "ads",
                "ad-",
                "banner",
                "menu",
                "nav",
                "sidebar",
                "footer",
                "comments",
                "related",
            ]
            for id_name in unwanted_ids:
                for tag in body_soup.find_all(id=lambda x: x and id_name in x.lower()):
                    tag.decompose()
            cleaned_html = body_soup.prettify()
        else:
            # bodyタグがない場合はHTMLの全テキストを返す
            for tag in soup.find_all(["script", "style"]):
                tag.decompose()
            cleaned_html = soup.prettify()

        cleaned_htmls.append(cleaned_html)
        logger.info("HTML整形処理完了")
        return cleaned_htmls


def search_brave(brave_api_key: str, keyword: str):
    """Brave APIで検索する

    Args:
        brave_api_key (str): Brave APIキー
        keyword (str): 検索キーワード

    Returns:
        list: 検索結果
    """

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": brave_api_key,
    }
    params = {
        "q": keyword,
        "count": 3,
        "text_decorations": 0,
        "country": "JP",
        "search_lang": "jp",
    }
    try:
        logger.info("検索開始")
        response = requests.get(
            f"https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        logger.info("検索完了")

        results = cleaned_html(response.json())
        return results
    except Exception as e:
        logger.exception(f"検索エラー: {e}")
        raise
