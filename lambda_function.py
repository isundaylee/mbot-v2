import os
import json
import logging

from lambdarest import lambda_handler
from mbot.handlers.relay import do_relay
from mbot.handlers.alertmanager import do_alertmanager


lambda_handler.handle("post", path="/relay")(do_relay)
lambda_handler.handle("post", path="/alertmanager")(do_alertmanager)
