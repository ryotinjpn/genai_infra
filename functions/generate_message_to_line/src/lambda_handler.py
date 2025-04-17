import bedrock
import line_api


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        # brave apiからニュースと天気を取得
        brave_response = "ネコが歩いていました。今日は天気です"
        messages = bedrock.generate_messages(brave_response)
        line_api.push_line_to_messages(messages)

        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
