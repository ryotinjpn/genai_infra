import logging
import os

import requests
import ssm

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def push_line_to_messages(messages: str):
    """LINEへプッシュメッセージを送信する

    Args:
        new_post (str): 投稿するポスト内容
    """

    channel_access_token = ssm.get_parameter_store_value(os.environ.get("LINE_API_CHANNEL_ACCESS_TOKEN"))
    target_id = ssm.get_parameter_store_value(os.environ.get("LINE_API_TARGET_ID"))
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": target_id,
        "messages": [
            {
                "type":"text",
                "text": messages
            }
        ]
    }
    try:
        logger.info("プッシュメッセージ送信開始")
        response = requests.post(
            "https://api.line.me/v2/bot/message/push", json=payload, headers=headers
        )
        response.raise_for_status()

        logger.info("プッシュメッセージ送信完了")
    except Exception as e:
        logger.exception(f"プッシュメッセージ送信エラー: {e}")
        raise
