import logging
import os
import uuid

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
agent_id = os.environ["BEDROCK_AGENT_ID"]
agent_alias_id = os.environ["BEDROCK_AGENT_ALIAS_ID"]


def generate_reply_message(input_text: str):
    """回答内容を生成する

    Args:
        input_text (str): メッセージ情報

    Returns:
        str: 回答内容
    """

    try:
        response = bedrock_agent_client.invoke_agent(
            inputText=input_text,
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=str(uuid.uuid1()),
            enableTrace=False,
        )
        results = response["completion"]
        for result in results:
            if "chunk" in result:
                generate_reply_message = result["chunk"]["bytes"].decode("utf-8")
        logger.info(generate_reply_message)
        logger.info("回答内容生成完了")

        return generate_reply_message
    except Exception as e:
        raise Exception(f"回答内容生成エラー: {e}")
