import os

from lambdarest import Response

from mbot.messenger import MessengerClient


def do_relay(event):
    data = event["json"]["body"]

    if (
        ("secret" not in data)
        or ("MBOT_RELAY_SECRET" not in os.environ)
        or (data["secret"] != os.environ["MBOT_RELAY_SECRET"])
    ):
        return Response(
            body={"success": False, "error": "No valid secret given."}, status_code=403
        )

    MessengerClient(access_token=os.environ["FB_PAGE_ACCESS_TOKEN"]).send_message(
        os.environ["FB_OWNER_ID"], data["message"]
    )

    return {"success": True}
