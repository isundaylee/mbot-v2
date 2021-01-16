import os
import json
import logging

import requests
from lambdarest import lambda_handler, Response


def send_message_to_owner(message):
    logging.info("Sending message: {}".format(message))
    request_body = {
        "recipient": {"id": os.environ.get("FB_OWNER_ID")},
        "message": {"text": message},
    }

    address = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(
        os.environ.get("FB_PAGE_ACCESS_TOKEN")
    )
    resp = requests.post(address, json=request_body)

    logging.info("Response: {} {}".format(resp.status_code, resp.json()))


@lambda_handler.handle("post", path="/relay")
def do_relay(event):
    if (
        ("secret" not in event)
        or ("MBOT_RELAY_SECRET" not in os.environ)
        or (event["secret"] != os.environ["MBOT_RELAY_SECRET"])
    ):
        return Response(
            body={"success": False, "error": "No valid secret given."}, status_code=403
        )

    send_message_to_owner(event["message"])

    return {"success": True}

