FROM public.ecr.aws/lambda/python:3.13

WORKDIR /var/task

COPY containers/lambda_invoke_gemini/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY functions/invoke_gemini/src .

CMD ["lambda_handler.lambda_handler"]
