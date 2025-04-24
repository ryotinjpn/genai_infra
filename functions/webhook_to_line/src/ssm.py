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
            Subject="【ALERT】lambda_webhook_to_line エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        raise Exception(f"パラメータストア取得エラー: {e}")


def update_ssm_parameter(target_id: str):
    """パラメータストアの値を更新する

    Args:
        target_id (str): 送信先ID
    """

    try:
        ssm_client.put_parameter(
            Name=os.environ.get("LINE_API_TARGET_ID"),
            Value=target_id,
            Type="SecureString",
            Overwrite=True,
        )
        logger.info("SSMパラメータ更新完了")
    except Exception as e:
        raise Exception(f"SSMパラメータ更新エラー: {e}")
