import base64
import json
import os
import urllib.parse
from datetime import datetime, timedelta, timezone

import boto3
import requests

ssm_client = boto3.client("ssm")
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = os.environ["MODEL_ID"]


def get_parameter_store_value(parameter_path: str):
    """パラメータストアに設定されている値を取得する
    パラメータストアのパスを指定して、対応する設定値を取得する
    前提:
        - NATゲートウェイを用いたインターネット通信が可能
        - AWS-Parameters-and-Secrets-Lambda-Extension レイヤーが存在する
    参考:
        - https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/ps-integration-lambda-extensions.html
    Args:
        parameter_path (str): SSMパラメータストアのパス
    Returns:
        str: パラメータストアに登録されている値
    """

    parameter_store_url = (
        "http://localhost:"
        + "2773"
        + "/systemsmanager/parameters/get/?name="
        + urllib.parse.quote_plus(parameter_path)
        + "&withDecryption=true"
    )
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN")}
    response = requests.get(parameter_store_url, headers=headers)
    return json.loads(response.text)["Parameter"]["Value"]


def update_ssm_parameter(new_refresh_token: str):
    """パラメータストアの値を更新する

    Args:
        new_refresh_token (str): リフレッシュトークン
    """

    try:
        ssm_client.put_parameter(
            Name=os.environ.get("X_API_REFRESH_TOKEN"),
            Value=new_refresh_token,
            Type="SecureString",
            Overwrite=True,
        )
        print("SSMパラメータ更新完了")
    except Exception as e:
        print(f"SSMパラメータ更新エラー: {e}")
        raise


def get_x_access_token():
    """アクセストークンを取得する

    Returns:
        str: アクセストークン
    """

    client_id = get_parameter_store_value(os.environ.get("X_API_CLIENT_ID"))
    client_secret = get_parameter_store_value(os.environ.get("X_API_CLIENT_SECRET"))
    refresh_token = get_parameter_store_value(os.environ.get("X_API_REFRESH_TOKEN"))

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    try:
        print("アクセストークン取得開始")
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
        update_ssm_parameter(new_refresh_token)

        print("アクセストークン取得完了")
        return access_token
    except Exception as e:
        print(f"アクセストークン取得エラー: {e}")
        raise


def print_x_rate_limit(headers):
    """レート制限エラーを出力する

    Args:
        headers (json): レスポンスヘッダー
    """

    limit = int(headers.get("x-rate-limit-limit"))
    remaining = int(headers.get("x-rate-limit-remaining"))
    print(f"エンドポイントレート制限上限: {limit}")
    print(f"5分間実行可能残リクエスト件数: {remaining}")

    reset = int(headers.get("x-rate-limit-reset"))
    reset_time_utc = datetime.fromtimestamp(reset, tz=timezone.utc)
    formatted_time = reset_time_utc.astimezone(timezone(timedelta(hours=9))).strftime(
        "%Y年%m月%d日 %H時%M分%S秒"
    )
    print(f"リセット時間（日本時間）: {formatted_time}")


def get_x_to_posts(access_token: str):
    """ポスト一覧を取得する

    Args:
        access_token (str): アクセストークン

    Returns:
        json: ポスト内容
    """

    user_id = get_parameter_store_value(os.environ.get("X_API_USER_ID"))
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    try:
        print("ポスト一覧得開始")
        response = requests.get(
            f"https://api.twitter.com/2/users/{user_id}/tweets",
            headers=headers,
            params={"max_results": "60"},
        )
        response.raise_for_status()

        print("ポスト一覧得完了")
        return response.json()
    except Exception as e:
        if response.status_code == 429:
            print_x_rate_limit(response.headers)
        print(f"ポスト一覧取得エラー: {e}")
        raise


def generate_post(posts: json):
    """ポスト内容を生成する

    Args:
        posts (json): ポスト一覧

    Returns:
        str: ポスト投稿内容
    """

    prompt = f"""
        あなたはAWSに関する知識を持つ高度な AI エージェントです。
        AWSドキュメントからランダムにトピックを選んで下さい。
        技術者向けに、高度なトピックを選んで要約して下さい。
        {posts}に含まれる内容は除外して下さい。
        タイトル以外は箇条書きにし、論文調にして下さい。
        参考にした日本語版AWSドキュメントURLを表示して下さい。
        日本語版AWSドキュメントURLがない場合英語版を表示して下さい。

        下記の形式で出力して下さい。

        【タイトル】
        ・要約
        AWSドキュメントURL

        タイトル、要約、AWSドキュメントURL含めて130文字以上140文字以下にして下さい。
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
        print(generate_post)

        return generate_post
    except Exception as e:
        print(f"ポスト投稿内容生成エラー: {e}")
        raise


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
        print("ポスト投稿開始")
        response = requests.post(
            "https://api.twitter.com/2/tweets", json=payload, headers=headers
        )
        response.raise_for_status()

        print("ポスト投稿完了")
    except Exception as e:
        if response.status_code == 429:
            print_x_rate_limit(response.headers)
        print(f"ポスト投稿エラー: {e}")
        raise


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        access_token = get_x_access_token()
        posts = get_x_to_posts(access_token)
        new_post = generate_post(posts)
        create_x_to_posts(access_token, new_post)

        return {"statusCode": 200, "message": "処理成功"}
    except Exception as e:
        return {"statusCode": 500, "message": "処理失敗", "error": str(e)}
