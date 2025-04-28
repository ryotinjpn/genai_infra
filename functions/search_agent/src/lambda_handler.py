import logging
import os
import traceback

import bedrock
import boto3
import brave_api
import google_news
import transformer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def get_keyword(parameters):
    """検索キーワードを取得する

    Args:
        parameters (list): イベントオブジェクトから取得したパラメータリスト

    Returns:
        str: 検索キーワード
    """

    return next(
        (param.get("value") for param in parameters if param.get("name") == "keyword"),
        None,
    )


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    function = event["function"]
    response_text = None
    try:
        match function:
            case "search_news":
                response_text = google_news.search_google_news_business()
            case "search_web":
                parameters = event.get("parameters", [])
                keyword = get_keyword(parameters)
                if not keyword:
                    response_text = "検索キーワードが指定されていません"
                else:
                    results = brave_api.search_brave(keyword)
                    cleaned_html = transformer.cleaned_html(results)
                    response_text = bedrock.generate_summary(keyword, cleaned_html)
            case _:
                response_text = "Error No function was called"
                logger.warning("関数未呼び出し")
    except Exception as e:
        response_text = "Error"
        error_message = f"\n{str(e)}\n\n{traceback.format_exc()}"
        logger.error(error_message)
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_search_agent エラー",
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
