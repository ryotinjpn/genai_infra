import logging
import os
import traceback

import boto3
import google_api

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def get_parameter(parameters, key):
    """タイトルを取得する

    Args:
        parameters (list): イベントオブジェクトから取得したパラメータリスト
        key (str): 取得したいパラメータのキー

    Returns:
        str: パラメータ
    """

    return next(
        (param.get("value") for param in parameters if param.get("name") == key),
        None,
    )


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    function = event["function"]
    response_text = None
    try:
        parameters = event.get("parameters", [])
        match function:
            case "create_event":
                summary = get_parameter(parameters, "summary")
                start = get_parameter(parameters, "start")
                end = get_parameter(parameters, "end")
                response_text = google_api.create_calendar_event(summary, start, end)
            case _:
                response_text = "Error No function was called"
                logger.warning("関数未呼び出し")
    except Exception as e:
        response_text = "Error"
        error_message = f"\n{str(e)}\n\n{traceback.format_exc()}"
        logger.error(error_message)
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_google_calenda_agent エラー",
            Message=error_message,
        )

    response_body = {"TEXT": {"body": response_text}}
    function_response = {
        "actionGroup": event["actionGroup"],
        "function": function,
        "functionResponse": {"responseBody": response_body},
    }
    action_response = {
        "messageVersion": "1.0",
        "response": function_response,
        "sessionAttributes": event["sessionAttributes"],
        "promptSessionAttributes": event["promptSessionAttributes"],
    }
    logger.info(action_response)
    return action_response
