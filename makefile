dist/mbot-relay.zip: mbot-relay/lambda_function.py
	cd mbot-relay; pip install --target ./packages -r requirements.txt
	cd mbot-relay/packages; zip -r ../../dist/mbot-relay.zip *
	cd mbot-relay/; zip -r ../dist/mbot-relay.zip lambda_function.py

deploy-mbot-relay: dist/mbot-relay.zip
	aws lambda update-function-code --region us-east-1 --function-name mbot-relay --zip-file fileb://dist/mbot-relay.zip

clean:
	rm dist/*.zip

