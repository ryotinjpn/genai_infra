import json
import os

import ssm

is_update_ssm_parameter = bool(int(os.environ["IS_UPDATE_SSM_PARAMETER"]))


def lambda_handler(event, _):
    """Lambdaエントリーポイント"""

    try:
        body = json.loads(event["body"])
        source_type = body["events"][0]["source"]["type"]

        match source_type:
            case "user":
                target_id = body["events"][0]["source"]["userId"]
            case "group":
                target_id = body["events"][0]["source"]["groupId"]
            case "room":
                target_id = body["events"][0]["source"]["roomId"]
            case _:
                return {"status_code": 400, "message": "不正なソースタイプ"}

        if is_update_ssm_parameter:
            ssm.update_ssm_parameter(target_id)

        return {"status_code": 200, "message": "処理成功"}
    except Exception as e:
        return {"status_code": 500, "message": "処理失敗", "error": str(e)}
