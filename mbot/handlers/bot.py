import os
import logging

from lambdarest import Response

from mbot.bot.features.google_apps_recorder import GoogleAppsRecorderFeature
from mbot.bot.bot import Bot
from mbot.messenger import MessengerClient
from mbot.utils.google_apps import GoogleApps


logger = logging.getLogger("mbot.handlers.bot")


def do_bot_get(event):
    args = event["json"]["query"]

    if (
        ("hub.mode" in args)
        and ("hub.verify_token" in args)
        and ("hub.challenge" in args)
    ):
        mode = args["hub.mode"]
        token = args["hub.verify_token"]
        challenge = args["hub.challenge"]

        if (mode == "subscribe") and (token == os.environ.get("FB_VERIFY_TOKEN")):
            return challenge

    return Response(body="403 Forbidden", status_code=403)


def do_bot_post(event):
    data = event["json"]["body"]

    logging.info("received %s", str(data))

    if data["object"] != "page":
        return ""

    bot = Bot(
        [
            GoogleAppsRecorderFeature(
                GoogleApps(
                    os.environ["MBOT_GA_CREDENTIALS"],
                    os.environ["MBOT_GA_BP_SPREADSHEET_ID"],
                )
            )
        ],
        MessengerClient(os.environ["FB_PAGE_ACCESS_TOKEN"]),
        os.environ["FB_OWNER_ID"],
    )

    for entry in data["entry"]:
        if "messaging" not in entry:
            continue

        for messaging in entry["messaging"]:
            if messaging["sender"]["id"] != os.environ.get("FB_OWNER_ID"):
                logging.warning(
                    "Ignored message from ID {}".format(messaging["sender"]["id"])
                )
                continue

            text = messaging["message"]["text"]

            logging.info("Processing message: %s", text)
            bot.process_message(text)

    return "EVENT_RECEIVED"
