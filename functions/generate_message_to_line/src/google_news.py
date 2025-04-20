import logging

import requests
from transformer import parse_google_news

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def search_google_news_business():
    """Google ニュースから最新ビジネス情報取得する

    Returns:
        str: ビジネス情報
    """

    try:
        logger.info("ビジネス情報取得開始")

        response = requests.get(
            "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtcGhHZ0pLVUNnQVAB?hl=ja&gl=JP&ceid=JP:ja",
        )
        response.raise_for_status()
        logger.info("ビジネス情報取得完了")

        result = parse_google_news(response.content)

        return result
    except Exception as e:
        logger.exception(f"ビジネス情報取得エラー: {e}")
        raise
