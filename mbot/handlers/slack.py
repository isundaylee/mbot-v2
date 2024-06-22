import functools
import json
import logging
import os
from typing import Any

from slack_sdk import signature
import slack_sdk

logger = logging.getLogger(__name__)


@functools.cache
def _get_slack_client() -> slack_sdk.WebClient:
    return slack_sdk.WebClient(os.environ["SLACK_BOT_USER_TOKEN"])


def _handle_event(event: dict[str, Any]) -> None:
    def _reply(message: str) -> None:
        client = _get_slack_client()
        client.chat_postMessage(
            channel=event["channel"], thread_ts=event["ts"], text=message
        )

    match event_type := event["type"]:
        case "message":
            if "bot_id" in event:
                return

            _reply("Hello you")
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
