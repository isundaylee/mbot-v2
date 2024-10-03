import logging
from typing import Any

import lambdarest
import prometheus_client

from mbot.handlers.relay import do_relay
from mbot.handlers.alertmanager import do_alertmanager
from mbot.handlers.bot import do_bot_get, do_bot_post
from mbot.handlers.slack import do_slack_post
from mbot.handlers.metrics import do_metrics

prom_request_count = prometheus_client.Counter(
    "mbot_v2_request_count",
    "Number of requests served by this particular AWS Lambda execution.",
)


def lambda_handler(*args: Any) -> Any:
    prom_request_count.inc()
    return lambdarest.lambda_handler(*args)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)-35s %(message)s",
    datefmt="%Y%m%d %H:%M:%S",
)

lambdarest.lambda_handler.handle("post", path="/relay")(do_relay)

lambdarest.lambda_handler.handle("post", path="/alertmanager")(do_alertmanager)

lambdarest.lambda_handler.handle("get", path="/webhook")(do_bot_get)
lambdarest.lambda_handler.handle("post", path="/webhook")(do_bot_post)

lambdarest.lambda_handler.handle("post", path="/slack")(do_slack_post)

lambdarest.lambda_handler.handle("get", path="/metrics")(do_metrics)
