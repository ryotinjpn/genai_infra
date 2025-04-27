import json
import logging
import os
import traceback

import bedrock
import boto3
import ssm
from linebot import LineBotApi
from linebot.models import TextSendMessage

logger = logging.getLogger()
logger.setLevel(logging.INFO)

IS_UPDATE_SSM_PARAMETER = bool(int(os.environ["IS_UPDATE_SSM_PARAMETER"]))

channel_access_token = ssm.get_parameter_store_value(
    os.environ.get("LINE_API_CHANNEL_ACCESS_TOKEN")
)

sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        body = json.loads(event["body"])
        events = body["events"][0]
        source_type = events["source"]["type"]

        match source_type:
            case "user":
                target_id = events["source"]["userId"]
            case "group":
                target_id = events["source"]["groupId"]
            case "room":
                target_id = events["source"]["roomId"]
            case _:
                return {"status_code": 400, "message": "不正なソースタイプ"}

        if IS_UPDATE_SSM_PARAMETER:
            ssm.update_ssm_parameter(target_id)

        if events["type"] != "message" or events["message"]["type"] != "text":
            logger.info("テキストメッセージではない")
            return {"status_code": 200, "message": "非テキストメッセージ"}

        mention = events["message"].get("mention", {})
        if not mention:
            logger.info("メンションなし")
            return {"status_code": 200, "message": "メンションなし"}

        is_mentioned = any(m.get("isSelf") for m in mention["mentionees"])
        if is_mentioned:
            logger.info("メンション受信")
            line_bot_api = LineBotApi(channel_access_token)

            reply_message = bedrock.generate_reply_message(events["message"]["text"])
            logger.info("回答内容生成完了")
            line_bot_api.reply_message(
                events["replyToken"], TextSendMessage(text=reply_message)
            )
            logger.info("メンション返信完了")
        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_webhook_to_line エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
