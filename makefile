dist/packages.zip: requirements.txt
	pip install --target dist/packages -r requirements.txt
	rm -f dist/packages.zip
	cd dist/packages; zip -r ../packages.zip *

dist/mbot.zip: dist/packages.zip lambda_function.py $(shell find mbot -type f)
	cp dist/packages.zip dist/mbot.zip
	zip -r dist/mbot.zip lambda_function.py
	zip -r dist/mbot.zip mbot

dist/mbot_backend.zip: dist/packages.zip lambda_function_backend.py $(shell find mbot -type f)
	cp dist/packages.zip dist/mbot_backend.zip
	zip -r dist/mbot_backend.zip lambda_function_backend.py
	zip -r dist/mbot_backend.zip mbot

.PHONY: deploy deploy_frontend deploy_backend clean

deploy: deploy_frontend deploy_backend

deploy_frontend: dist/mbot.zip
	aws lambda update-function-code --region us-east-1 --function-name mbot --zip-file fileb://dist/mbot.zip

deploy_backend: dist/mbot_backend.zip
	aws lambda update-function-code --region us-east-1 --function-name mbot_backend --zip-file fileb://dist/mbot_backend.zip

clean:
	rm -r dist/*

