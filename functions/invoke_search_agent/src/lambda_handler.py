import logging
import os
import traceback
import uuid

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
agent_id = os.environ["BEDROCK_AGENT_ID"]
agent_alias_id = os.environ["BEDROCK_AGENT_ALIAS_ID"]

sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    input_text = event.get("input_text", None)
    if not input_text:
        logger.error("inputText がイベントから取得できませんでした")
        return {"status_code": 400, "message": "inputText が必要です"}

    try:
        response = bedrock_agent_client.invoke_agent(
            inputText=input_text,
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=str(uuid.uuid1()),
            enableTrace=False,
        )
        logger.info(response)
        results = response["completion"]
        for result in results:
            if "chunk" in result:
                data = result["chunk"]["bytes"].decode("utf-8")
        logger.info(data)

        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_generate_message_to_line エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
