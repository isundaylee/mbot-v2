import os
import json
import logging

from lambdarest import lambda_handler
from mbot.handlers.relay import do_relay
from mbot.handlers.alertmanager import do_alertmanager
from mbot.handlers.bot import do_bot_get, do_bot_post
from mbot.handlers.slack import do_slack_post


logging.getLogger().setLevel(logging.INFO)
for handler in logging.getLogger().handlers:
    handler.setFormatter(
        logging.Formatter(fmt="%(levelname)s - %(name)s - %(message)s")
    )

lambda_handler.handle("post", path="/relay")(do_relay)

lambda_handler.handle("post", path="/alertmanager")(do_alertmanager)

lambda_handler.handle("get", path="/webhook")(do_bot_get)
lambda_handler.handle("post", path="/webhook")(do_bot_post)

lambda_handler.handle("post", path="/slack")(do_slack_post)
