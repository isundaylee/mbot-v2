import os
from mbot.bot.action_kit import BaseActionKit
from mbot.bot.features.google_apps_recorder import (
    BaseFeature,
    GoogleAppsRecorderFeature,
)
from mbot.utils.google_apps import GoogleApps
from mbot.utils.messenger import MessengerClient


def build_default_features() -> list[BaseFeature]:
    return [
        GoogleAppsRecorderFeature(
            GoogleApps(
                os.environ["MBOT_GA_CREDENTIALS"],
                os.environ["MBOT_GA_BP_SPREADSHEET_ID"],
            )
        )
    ]


class Bot:
    def __init__(self, features, action_kit: BaseActionKit):
        self.features = features
        self.action_kit = action_kit

    def process_message(self, message: str) -> None:
        for feature in self.features:
            if feature.process(message, self.action_kit):
                return

        self.action_kit.send_message_to_owner("Sorry, I don't understand ):")
