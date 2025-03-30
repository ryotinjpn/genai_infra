import bedrock
import dynamodb
import xapi

dynamodb_resource = dynamodb.DynamoDBResource()


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        post_history = dynamodb_resource.get_post_history()
        new_post = bedrock.generate_post(post_history)
        access_token = xapi.get_x_access_token()
        xapi.create_x_to_posts(access_token, new_post)
        dynamodb_resource.put_post_history(new_post)

        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
