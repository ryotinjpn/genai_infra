import logging
import os
import traceback

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm_client = boto3.client("ssm")
sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def get_parameter_store_value(parameter_path: str):
    """パラメータストアに設定されている値を取得する
    パラメータストアのパスを指定して、対応する設定値を取得する

    Args:
        parameter_path (str): SSMパラメータストアのパス
    Returns:
        str: パラメータストアに登録されている値
    """

    try:
        response = ssm_client.get_parameter(Name=parameter_path, WithDecryption=True)
        return response["Parameter"]["Value"]
    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_search_agent エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        raise Exception(f"パラメータストア取得エラー: {e}")


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
