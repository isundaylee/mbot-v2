import logging

import requests


class MessengerClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def send_message(self, recipient_id, message):
        address = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(
            self.access_token
        )
        resp = requests.post(
            address,
            json={"recipient": {"id": recipient_id}, "message": {"text": message}},
        )

        logging.info(
            "Messenger_Client.send_message response: {} {}".format(
                resp.status_code, resp.json()
            )
        )
