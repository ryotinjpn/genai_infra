import os

import bedrock
import brave_api
import line_api
import ssm


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        brave_api_key = ssm.get_parameter_store_value(os.environ.get("BRAVE_API_KEY"))
        result = brave_api.search_brave(brave_api_key, "現在 神戸 天気")

        prompt = bedrock.get_weather_prompt(result)
        messages = bedrock.generate_messages(prompt)

        line_api.push_line_to_messages(messages)

        result = brave_api.search_brave(brave_api_key, "現在 ビジネス ニュース")

        prompt = bedrock.get_news_prompt(result[0])
        messages = bedrock.generate_messages(prompt)

        line_api.push_line_to_messages(messages)

        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
