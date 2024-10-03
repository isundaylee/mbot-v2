import logging

import prometheus_client

from typing import Any

logger = logging.getLogger(__name__)


def do_metrics(event: dict[str, Any]) -> str:
    logging.info("Handling metrics request")
    return prometheus_client.generate_latest().decode()
