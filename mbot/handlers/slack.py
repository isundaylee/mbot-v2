import json
import logging
import os
from typing import Any

from slack_sdk import signature
import slack_sdk

logger = logging.getLogger(__name__)


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
        case _:
            raise RuntimeError(f"Invalid request type {request_type}")

    # client = slack_sdk.WebClient(os.environ["SLACK_BOT_USER_TOKEN"])
