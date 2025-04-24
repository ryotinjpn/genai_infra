import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_client = boto3.client("bedrock-runtime")
model_id = os.environ["MODEL_ID"]


def generate_summary(keyword: str, text: str):
    """要約を生成する

    Args:
        text (str): 元テキスト

    Returns:
        str: 要約内容
    """

    prompt = f"""
        あなたはテキスト抽出と要約能力持つ高度な AI エージェントです

        {text}
        上記のテキストから「{keyword}」に関連する情報を抽出し要約して下さい

        下記の形式で出力して下さい
        要約毎に箇条書きし改行して下さい
        箇条書き毎に要約文と要約元URLを記載して下さい

        要約、要約元URL含めて文字300文字以下にして下さい
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
        generate_summary = response_body["content"][0]["text"]
        logger.info(generate_summary)

        return generate_summary
    except Exception as e:
        raise Exception(f"要約生成エラー: {e}")
