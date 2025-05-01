setup:
	brew install tfenv
	tfenv install 1.10.5
	tfenv use 1.10.5
	brew install aws-vault
	brew install --cask google-cloud-sdk
	brew install tflint
	brew install aquasecurity/trivy/trivy

test:
	terraform fmt -recursive
	terraform validate
	tflint --init
	tflint
	trivy config . --config trivy.yaml --ignorefile .trivyignore

LAYER_DIRS := common
layer:
	@for layer in $(LAYER_DIRS); do \
		echo "Building layer: $$layer"; \
		rm -rf lambda_layers/$$layer/lambda_layer.zip; \
		mkdir -p lambda_layers/temp_layer/python; \
		pip install -r lambda_layers/$$layer/requirements.txt -t lambda_layers/temp_layer/python; \
		(cd lambda_layers/temp_layer && zip -r ../$$layer/lambda_layer.zip .); \
		rm -rf lambda_layers/temp_layer; \
	done

CONTAINER_DIRS := lambda_invoke_gemini
lambda_build:
	@for container in $(CONTAINER_DIRS); do \
		echo "Building container: $$container"; \
		docker buildx build --platform linux/amd64 --no-cache \
			-t genai/$$container \
			-f containers/$$container/Dockerfile .; \
	done

format-py:
	black .
	isort .
