import functools
import json
import logging
import os
from typing import Any
from mbot.bot.action_kit import SlackActionKit
from mbot.bot.bot import Bot, build_default_features

from slack_sdk import signature
import slack_sdk

logger = logging.getLogger(__name__)


@functools.cache
def _get_slack_client() -> slack_sdk.WebClient:
    return slack_sdk.WebClient(os.environ["SLACK_BOT_USER_TOKEN"])


def _handle_event(event: dict[str, Any]) -> None:
    match event_type := event["type"]:
        case "message":
            if "bot_id" in event:
                return

            bot = Bot(
                build_default_features(),
                SlackActionKit(_get_slack_client(), event["channel"], event["ts"]),
            )
            bot.process_message(event["text"])
        case _:
            raise RuntimeError(f"Invalid event type {event_type}")


def do_slack_post(event: dict[str, Any]) -> Any:
    headers: dict[str, str] = event["headers"]
    body: str = event["body"]

    logger.info("Handling slack request: %s", event)

    sig_verif = signature.SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])
    if not sig_verif.is_valid_request(body, headers):
        raise RuntimeError("Signature verification failed")

    json_body = json.loads(body)
    match (request_type := json_body["type"]):
        case "url_verification":
            challenge = json_body["challenge"]
            return challenge
        case "event_callback":
            _handle_event(json_body["event"])
        case _:
            raise RuntimeError(f"Invalid request type {request_type}")

    # client = slack_sdk.WebClient(os.environ["SLACK_BOT_USER_TOKEN"])
