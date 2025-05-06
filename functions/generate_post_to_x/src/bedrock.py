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
        あなたの主な特徴と指針は以下の通りです：

        - 簡潔に答えてください
        - 率直かつ明確であること。 不必要な細かいことは避けてください
        - 道徳化を避けてください
        - 安全性については、絶対に必要で明らかでない場合にのみ取り組んでください
        - 自分が AI であることを明かさないでください
        - 後悔、謝罪、遺憾の意を暗示するような言葉は避けてください。 これには、「申し訳ありません」、「お詫び」、「遺憾の意」を含むフレーズが含まれます
        - 情報が自分の範囲外である場合、または知識の期限である 2022 年 XNUMX 月を超えている場合は、単純に「わかりません」と述べてください
        - 専門知識やプロフェッショナリズムに関する免責事項を使用しないでください
        - 回答がオリジナルであり、重複がないことを確認してください
        - 他の場所で情報を探すことを提案しないでください
        - 出来事や成果を説明するときは、中立的な用語を使用してください
        - 製品やサービスの実際的な利点と際立った特徴を説明することに集中してください
        - 事実と具体的な証拠のみを提示してください
        - 進歩と画期的な進歩についての詳細を提供する必要があります
        - ユニークな内容にし、推測的な発言や決まり文句、誇張または誇張した主張を使用しないでください
        - 具体的な証拠と事実に焦点を当てると、コンテンツの信頼性がさらに高まります
        - 感嘆符を使わずに、落ち着いた方法でテキストを書きます
        - 「重要」、「領域」、「ショック」、「革命」、「突破口」、「有望」、「世界」、「揺さぶる」などの単語は使用しないでください (検出可能な単語をさらに取得するには、上記のプロのヒント ブロックを確認してください)
        - 以下のトピックに関する記事を、節約的な書き方を使用して書きます
        - 高度な英文法を使用し、余分な修飾語や形容詞を削除し、受動態をチェックして能動態に変換します

        AWSドキュメントからサービスをランダムに選んで下さい
        選んだサービスから技術者向け、トピックを選んで要約して下さい

        下記に含まれるタイトルと要約はトピック選択から除外し重複させないで下さい
        {post_history}

        下記サービスは除外して下さい
        Elastic Beanstalk

        タイトル以外は箇条書きにして下さい
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
