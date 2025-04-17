import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm_client = boto3.client("ssm")


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
        logger.exception(f"SSMパラメータ更新エラー: {e}")
        raise
