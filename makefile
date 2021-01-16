dist/mbot.zip: lambda_function.py requirements.txt
	pip install --target dist/packages -r requirements.txt
	rm -f dist/mbot.zip
	cd dist/packages; zip -r ../mbot.zip *
	zip -r dist/mbot.zip lambda_function.py

deploy: dist/mbot.zip
	aws lambda update-function-code --region us-east-1 --function-name mbot --zip-file fileb://dist/mbot.zip

clean:
	rm dist/*.zip

