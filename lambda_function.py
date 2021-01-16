import os
import json
import logging

from lambdarest import lambda_handler
from mbot.handlers.relay import do_relay
from mbot.handlers.alertmanager import do_alertmanager


logging.getLogger().setLevel(logging.INFO)
for handler in logging.getLogger().handlers:
    handler.setFormatter(logging.Formatter(fmt="%(levelname)s %(message)s"))

lambda_handler.handle("post", path="/relay")(do_relay)
lambda_handler.handle("post", path="/alertmanager")(do_alertmanager)
