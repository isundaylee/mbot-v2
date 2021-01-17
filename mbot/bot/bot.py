from mbot.bot.action_kit import ActionKit
from mbot.utils.messenger import MessengerClient


class Bot:
    def __init__(self, features, messenger_client: MessengerClient, owner_id: str):
        self.features = features
        self.action_kit = ActionKit(messenger_client, owner_id)

    def process_message(self, message: str) -> None:
        for feature in self.features:
            if feature.process(message, self.action_kit):
                return

        self.action_kit.send_message_to_owner("Sorry, I don't understand ):")

