import json
import logging
import os
import urllib.parse

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm_client = boto3.client("ssm")


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
        logger.info("SSMパラメータ更新完了")
    except Exception as e:
        logger.exception(f"SSMパラメータ更新エラー: {e}")
        raise
