import base64
import logging
import os
from datetime import datetime, timedelta, timezone

import requests
import ssm

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_x_access_token():
    """アクセストークンを取得する

    Returns:
        str: アクセストークン
    """

    client_id = ssm.get_parameter_store_value(os.environ.get("X_API_CLIENT_ID"))
    client_secret = ssm.get_parameter_store_value(os.environ.get("X_API_CLIENT_SECRET"))
    refresh_token = ssm.get_parameter_store_value(os.environ.get("X_API_REFRESH_TOKEN"))

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    try:
        logger.info("アクセストークン取得開始")
        response = requests.post(
            "https://api.twitter.com/2/oauth2/token", headers=headers, data=data
        )
        response.raise_for_status()

        access_token = response.json().get("access_token")
        if not access_token:
            raise ValueError("アクセストークン取得できませんでした")

        new_refresh_token = response.json().get("refresh_token")
        if not new_refresh_token:
            raise ValueError("リフレッシュトークン取得できませんでした")
        ssm.update_ssm_parameter(new_refresh_token)

        logger.info("アクセストークン取得完了")
        return access_token
    except Exception as e:
        logger.exception(f"アクセストークン取得エラー: {e}")
        raise


def log_x_rate_limit(headers):
    """レート制限エラーを出力する

    Args:
        headers (json): レスポンスヘッダー
    """

    limit = int(headers.get("x-rate-limit-limit"))
    remaining = int(headers.get("x-rate-limit-remaining"))
    logger.warning(f"エンドポイントレート制限上限: {limit}")
    logger.warning(f"5分間実行可能残リクエスト件数: {remaining}")

    reset = int(headers.get("x-rate-limit-reset"))
    reset_time_utc = datetime.fromtimestamp(reset, tz=timezone.utc)
    formatted_time = reset_time_utc.astimezone(timezone(timedelta(hours=9))).strftime(
        "%Y年%m月%d日 %H時%M分%S秒"
    )
    logger.warning(f"リセット時間（日本時間）: {formatted_time}")


def create_x_to_posts(access_token: str, new_post: str):
    """ポスト投稿をする

    Args:
        access_token (str): アクセストークン
        new_post (str): 投稿するポスト内容
    """

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"for_super_followers_only": False, "nullcast": False, "text": new_post}
    try:
        logger.info("ポスト投稿開始")
        response = requests.post(
            "https://api.twitter.com/2/tweets", json=payload, headers=headers
        )
        response.raise_for_status()

        logger.info("ポスト投稿完了")
    except Exception as e:
        if response.status_code == 429:
            log_x_rate_limit(response.headers)
        logger.exception(f"ポスト投稿エラー: {e}")
        raise
