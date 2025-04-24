import os
import traceback

import bedrock
import boto3
import dynamodb
import x_api

dynamodb_resource = dynamodb.DynamoDBResource()
sns_client = boto3.client("sns")
sns_topic_arn = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        post_history = dynamodb_resource.get_post_history()
        new_post = bedrock.generate_post(post_history)
        x_api.create_x_to_posts(new_post)
        dynamodb_resource.put_post_history(new_post)

        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="【ALERT】lambda_generate_post_to_x エラー",
            Message=f"\n{str(e)}\n\n{traceback.format_exc()}",
        )
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
