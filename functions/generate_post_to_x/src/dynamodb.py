import logging
from datetime import datetime, timedelta

import boto3
from ulid import ULID

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DynamoDBResource:
    def __init__(self):
        self.dynamodb_resource = boto3.resource("dynamodb").Table(
            "GeneratePostToXHistory"
        )

    def get_post_history(self):
        """DynamoDBからポスト投稿履歴を取得する

        Returns:
            str: ポスト投稿履歴
        """

        try:
            response = self.dynamodb_resource.scan()
            items = response.get("Items", [])
            post_histories = [item.get("PostContent") for item in items]
            post_histories = "\n".join(post_histories)
            logger.info(post_histories)
            return post_histories
        except Exception as e:
            logger.exception(f"DynamoDBポスト投稿履歴取得エラー: {e}")
            raise

    def put_post_history(self, post: str):
        """DynamoDBへポスト投稿内容保存

        Args:
            post (str): ポスト投稿内容
        """

        now = datetime.now()
        try:
            self.dynamodb_resource.put_item(
                Item={
                    "HistoryId": str(ULID()),
                    "PostContent": post,
                    "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "ExpireAt": int((now + timedelta(days=30)).timestamp()),
                }
            )
            logger.info("DynamoDBポスト投稿内容保存完了")
        except Exception as e:
            logger.exception(f"DynamoDBポスト投稿内容保存エラー: {e}")
            raise
