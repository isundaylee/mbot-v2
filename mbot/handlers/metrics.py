import logging

import prometheus_client
from lambdarest import Response

from typing import Any

logger = logging.getLogger(__name__)


def do_metrics(event: dict[str, Any]) -> str:
    logging.info("Handling metrics request")
    return Response(
        body=prometheus_client.generate_latest().decode(),
        headers={"Content-Type": prometheus_client.CONTENT_TYPE_LATEST},
    )
