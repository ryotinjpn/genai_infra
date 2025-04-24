import os
import traceback

import bedrock
import boto3
import brave_api
import google_news
import line_api
import ssm

sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        brave_api_key = ssm.get_parameter_store_value(os.environ.get("BRAVE_API_KEY"))
        result = brave_api.search_brave(brave_api_key, "最新 神戸 天気")

        prompt = bedrock.get_weather_prompt(result)
        weather_messages = bedrock.generate_messages(prompt)

        result = google_news.search_google_news_business()

        prompt = bedrock.get_news_prompt(result)
        news_messages = bedrock.generate_messages(prompt)

        messages = f"{weather_messages}\n\n{news_messages}"

        line_api.push_line_to_messages(messages)

        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_generate_message_to_line エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
