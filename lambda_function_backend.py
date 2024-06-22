import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Handling event %s with context %s", event, context)
    return {"success": True}
