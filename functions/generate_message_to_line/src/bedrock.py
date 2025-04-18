import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = os.environ["MODEL_ID"]


def get_weather_prompt(text: str):
    """天気情報を要約するプロンプトを生成する

    Args:
        text (str): 天気情報

    Returns:
        str: 天気情報を要約するプロンプト
    """

    return f"""
        あなたは天気情報に関する知識を持つ私の親しい友人です。フランクでカジュアルな感じで、話してください
        次のHTML文書はWebページの本文です
        次のHTML文書は天気情報です
        HTMLタグの構造を参考にしながら、セクションごとの重要な情報を要約して下さい

        {text}

        要約は適切に改行を行い読みやすくして下さい
        要約はあいさつなしで本題から始めて下さい
        要約は絵文字も利用してポップな形式にして下さい
        タイトルに天気情報の絵文字を入れて下さい
        タイトルの前に#を入れないで下さい
        以上を考慮し下記の形式で出力して下さい
        【タイトル】
        要約

        タイトル、要約含めて130文字以上140文字以下にして下さい
    """


def get_news_prompt(text: str):
    """ニュース情報を要約するプロンプトを生成する

    Args:
        text (str): ニュース情報

    Returns:
        str: ニュース情報を要約するプロンプト
    """

    return f"""
        あなたは社会情勢について知識を持つ高度な AI エージェントです
        次のHTML文書はWebページの本文です
        次のHTML文書はニュース情報です
        HTMLタグの構造を参考にしながら、セクションごとの重要な情報を要約して下さい

        {text}

        セクションごとに要約して下さい
        要約は適切に改行を行い読みやすくして下さい
        要約はあいさつなしで本題から始めて下さい
        タイトルの前に#を入れないで下さい
        以上を考慮し下記の形式で出力して下さい
        【タイトル】
        要約
        参考先

        タイトル、要約含めて280文字以上300文字以下にして下さい
    """


def generate_messages(text: str):
    """メッセージ内容を生成する

    Args:
        text (str): メッセージ内容元情報

    Returns:
        str: ポスト投稿内容
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
                    "content": [{"type": "text", "text": text}],
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
