import functools
import logging
import os
from typing import Any
from mbot.bot.action_kit import SlackActionKit

from mbot.bot.bot import Bot, build_default_features
import slack_sdk

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@functools.cache
def _get_slack_client() -> slack_sdk.WebClient:
    return slack_sdk.WebClient(os.environ["SLACK_BOT_USER_TOKEN"])


def _handle_slack_event(event: dict[str, Any]) -> None:
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


def lambda_handler(event, context):
    logger.info("Handling event %s with context %s", event, context)

    match request_type := event["request_type"]:
        case "slack_event":
            _handle_slack_event(event["slack_event"])
        case _:
            raise RuntimeError(f"Unknown request type {request_type}")

    return {"success": True}
