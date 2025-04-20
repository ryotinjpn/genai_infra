import logging

import requests
from transformer import cleaned_html

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        "count": 1,
        "text_decorations": 0,
        "country": "JP",
        "search_lang": "jp",
    }
    try:
        logger.info("検索開始")
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
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
