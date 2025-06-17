import logging
import os
import json

import ssm
from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger()
logger.setLevel(logging.INFO)

credentials_json = ssm.get_parameter_store_value(
    os.environ.get("GOOGLE_APPLICATION_SERVICE_CREDENTIALS_PATH")
)

def create_calendar_event(summary: str, start: str, end: str):
    """
    Googleカレンダーに予定を作成する

    Args:
        summary (str): イベントのタイトル
        start (str): ISO8601形式の開始日時
        end (str): ISO8601形式の終了日時
    """

    try:
        credentials_dict = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=["https://www.googleapis.com/auth/calendar"]
        )

        service = build("calendar", "v3", credentials=credentials)
        event = {
            "summary": summary,
            "start": {"dateTime": start, "timeZone": "Asia/Tokyo"},
            "end": {"dateTime": end, "timeZone": "Asia/Tokyo"},
        }
        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )

        logger.info(f"カレンダー登録成功: {created_event.get('htmlLink')}")
        return created_event
    except Exception as e:
        logger.error(f"カレンダー登録エラー: {e}")
        raise
