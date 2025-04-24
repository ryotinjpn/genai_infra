import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = os.environ["MODEL_ID"]


def generate_post(post_history: str):
    """ポスト内容を生成する

    Args:
        post_history (str): ポスト投稿履歴

    Returns:
        str: ポスト投稿内容
    """

    prompt = f"""
        あなたはAWSに関する知識を持つ高度な AI エージェントです
        AWSドキュメントからサービスをランダムに選んで下さい
        選んだサービスから技術者向け、トピックを選んで要約して下さい

        下記に含まれるタイトルと要約はトピック選択から除外し重複させないで下さい
        {post_history}

        下記サービスは除外して下さい
        Elastic Beanstalk

        タイトル以外は箇条書きにし、論文調にして下さい
        参考にした日本語版AWSドキュメントURLを表示して下さい

        下記の形式で出力して下さい
        【タイトル】
        ・要約
        AWSドキュメントURL

        タイトル、要約、AWSドキュメントURL含めて130文字以上140文字以下にして下さい
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
        raise Exception(f"ポスト投稿内容生成エラー: {e}")
