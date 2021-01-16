dist/packages.installed: requirements.txt
	pip install --target dist/packages -r requirements.txt
	touch dist/packages.installed

dist/mbot.zip: dist/packages.installed lambda_function.py $(shell find mbot -type f)
	rm -f dist/mbot.zip
	cd dist/packages; zip -r ../mbot.zip *
	zip -r dist/mbot.zip lambda_function.py
	zip -r dist/mbot.zip mbot

deploy: dist/mbot.zip
	aws lambda update-function-code --region us-east-1 --function-name mbot --zip-file fileb://dist/mbot.zip

clean:
	rm dist/*.zip

