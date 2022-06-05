import logging

import requests


logger = logging.getLogger("mbot.utils.messenger")


class MessengerClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def send_message(self, recipient_id, message):
        address = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(
            self.access_token
        )
        resp = requests.post(
            address,
            json={
                "recipient": {"id": recipient_id},
                "message": {"text": message},
                "message_type": "MESSAGE_TAG",
                "tag": "ACCOUNT_UPDATE",
            },
        )
        resp.raise_for_status()

        logger.info(
            "send_message() got response: {} {}".format(resp.status_code, resp.json())
        )
