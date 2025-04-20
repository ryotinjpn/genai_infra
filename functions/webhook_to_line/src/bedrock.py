import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = os.environ["MODEL_ID"]


def generate_reply_message(text: str):
    """回答内容を生成する

    Args:
        text (str): メッセージ情報

    Returns:
        str: 回答内容
    """

    prompt = f"""
        あなたは私の親しい弟です
        あなたに下記のメッセージが届きました

        {text}

        メッセージの内容をよく理解して下さい
        敬意を持ちながらも、カジュアルな感じで返事をして下さい
        絵文字も利用して下さい
        あいさつなしで本題から始めて下さい

        130文字以上140文字以下にして下さい
        適切に改行を入れて下さい
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
        generate_reply_message = response_body["content"][0]["text"]
        logger.info(generate_reply_message)

        return generate_reply_message
    except Exception as e:
        logger.exception(f"回答内容生成エラー: {e}")
        raise
