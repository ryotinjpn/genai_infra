import logging
import os

import requests
import ssm

logger = logging.getLogger()
logger.setLevel(logging.INFO)

brave_api_key = ssm.get_parameter_store_value(os.environ.get("BRAVE_API_KEY"))


def search_brave(keyword: str):
    """Brave APIで検索する

    Args:
        keyword (str): 検索キーワード

    Returns:
        list: 検索結果
    """

    logger.info(f"検索キーワード: {keyword}")
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

        return response.json()
    except Exception as e:
        raise Exception(f"検索エラー: {e}")
