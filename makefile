dist/packages.zip: requirements.txt
	pip install --target dist/packages -r requirements.txt
	rm -f dist/packages.zip
	cd dist/packages; zip -r ../packages.zip *

dist/mbot.zip: dist/packages.zip lambda_function.py $(shell find mbot -type f)
	cp dist/packages.zip dist/mbot.zip
	zip -r dist/mbot.zip lambda_function.py
	zip -r dist/mbot.zip mbot

deploy: dist/mbot.zip
	aws lambda update-function-code --region us-east-1 --function-name mbot --zip-file fileb://dist/mbot.zip

clean:
	rm -r dist/*

