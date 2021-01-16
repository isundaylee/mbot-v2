import os
import json
import logging

import requests
from lambdarest import lambda_handler, Response

from mbot.messenger import MessengerClient


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

    MessengerClient(access_token=os.environ["FB_PAGE_ACCESS_TOKEN"]).send_message(
        os.environ["FB_OWNER_ID"], event["message"]
    )

    return {"success": True}

