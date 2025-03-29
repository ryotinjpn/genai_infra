setup:
	brew install tfenv
	tfenv install 1.10.5
	tfenv use 1.10.5
	brew install aws-vault
	brew install tflint
	brew install aquasecurity/trivy/trivy

test:
	terraform fmt -recursive
	terraform validate
	tflint --init
	tflint
	trivy config . --config trivy.yml --ignorefile .trivyignore

layer:
	rm -rf functions/lambda_layer.zip 
	mkdir -p functions/temp_layer/python
	pip install -r functions/requirements.txt -t functions/temp_layer/python
	cd functions/temp_layer && zip -r ../lambda_layer.zip .
	cd functions && rm -rf temp_layer

format-py:
	black .
	isort .
