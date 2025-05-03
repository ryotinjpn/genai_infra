import logging
import os
import traceback

import boto3
import vertex_ai

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    input_text = event.get("input_text", None)
    if not input_text:
        logger.error("input_text がイベントから取得できませんでした")
        return {"status_code": 400, "message": "input_text が必要です"}

    try:
        results = vertex_ai.generate_answer(input_text)

        return {"status_code": 200, "message": "処理成功", "text": results}
    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_invoke_gemini エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
