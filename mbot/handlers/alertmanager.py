import logging
import os

from mbot.messenger import MessengerClient


logger = logging.getLogger("mbot.handlers.alertmanager")


def do_alertmanager(event):
    data = event["json"]["body"]

    for alert in data["alerts"]:
        labels = alert["labels"].copy()
        del labels["alertname"]

        label_summary = ", ".join("{}={}".format(k, v) for k, v in labels.items())

        message = "Alertmanager: Alert {} is {}. Labels: {}. Source: {}".format(
            alert["labels"]["alertname"],
            alert["status"],
            label_summary,
            alert["generatorURL"],
        )

        logger.info("Sending message: {}".format(message))

        MessengerClient(access_token=os.environ["FB_PAGE_ACCESS_TOKEN"]).send_message(
            os.environ["FB_OWNER_ID"], message
        )

    return {"success": True}
