import json
import logging
import os
from typing import Any

from slack_sdk import signature
import boto3

logger = logging.getLogger(__name__)


def _handle_event(event: dict[str, Any]) -> None:
    boto_client = boto3.client("lambda")
    response = boto_client.invoke(
        FunctionName="mbot_backend",
        InvocationType="Event",
        Payload=json.dumps({"request_type": "slack_event", "slack_event": event}),
    )

    logger.info("Response from mbot_backend invocation: %s", response)

    if response["ResponseMetadata"]["HTTPStatusCode"] != 202:
        raise RuntimeError(
            f"Unexpected response from invoking mbot_backend: {response}"
        )


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
