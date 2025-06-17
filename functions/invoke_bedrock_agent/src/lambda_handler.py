import logging
import os
import traceback
import uuid

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_agent_client = boto3.client("bedrock-agent-runtime")

sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    required_keys = ["input_text", "agent_id", "agent_alias_id"]
    for key in required_keys:
        if not event.get(key):
            logger.error(f"イベントに {key} 未定義")
            return {"status_code": 400, "message": f"イベントに {key} 未定義"}

    try:
        response = bedrock_agent_client.invoke_agent(
            inputText=event["input_text"],
            agentId=event["agent_id"],
            agentAliasId=event["agent_alias_id"],
            sessionId=str(uuid.uuid1()),
            enableTrace=False,
        )
        logger.info(response)
        results = response["completion"]
        for result in results:
            if "chunk" in result:
                data = result["chunk"]["bytes"].decode("utf-8")
        logger.info(data)

        return {"status_code": 200, "message": "処理成功", "result": data}
    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】invoke_bedrock_agent エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
