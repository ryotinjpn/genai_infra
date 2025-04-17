import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = os.environ["MODEL_ID"]


def generate_messages(brave_response: str):
    """メッセージ内容を生成する

    Args:
        brave_response (str): brave apiから取得した情報

    Returns:
        str: ポスト投稿内容
    """

    prompt = f"""
        下記を要約してください
        {brave_response}

        130文字以上140文字以下にして下さい
    """

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "temperature": 0.6,
            "top_p": 0.8,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }
    )
    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
            body=body,
        )
        response_body = json.loads(response["body"].read())
        generate_post = response_body["content"][0]["text"]
        logger.info(generate_post)

        return generate_post
    except Exception as e:
        logger.exception(f"メッセージ内容生成エラー: {e}")
        raise
