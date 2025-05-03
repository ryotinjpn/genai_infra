import logging
import os

import ssm
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

model_id = os.environ["MODEL_ID"]
gcp_project_id = os.environ.get("GCP_PROJECT_ID")

credentials = ssm.get_parameter_store_value(
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH")
)

credentials_path = "/tmp/google-credentials.json"
with open(credentials_path, "w") as f:
    f.write(credentials)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


def generate_answer(text: str):
    """Vertex AI (Gemini) から回答を生成する

    Args:
        text (str): 元テキスト

    Returns:
        str: 回答内容
    """

    try:
        vertexai.init(project=gcp_project_id, location="us-central1")
        model = GenerativeModel(model_id)
        generation_config = GenerationConfig(
            temperature=0.9,
            top_k=40,
            top_p=0.9,
            candidate_count=1,
            max_output_tokens=8192,
        )

        response = model.generate_content(
            text,
            generation_config=generation_config,
        )
        logger.info("回答生成完了")
        logger.info(response.text)

        return response.text
    except Exception as e:
        raise Exception(f"回答生成エラー: {e}")
