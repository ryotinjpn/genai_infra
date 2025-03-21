setup:
	brew install tfenv
	brew install tflint
	brew install aquasecurity/trivy/trivy

test:
	terraform fmt -recursive
	terraform validate
	tflint --init
	tflint
	trivy config . --config trivy.yml --ignorefile .trivyignore

layer:
	rm -rf files/lambda/lambda_layer.zip 
	mkdir -p files/lambda/temp_layer/python
	pip install -r files/lambda/requirements.txt -t files/lambda/temp_layer/python
	cd files/lambda/temp_layer && zip -r ../lambda_layer.zip .
	cd files/lambda && rm -rf temp_layer
