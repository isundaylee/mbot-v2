from mbot.utils.messenger import MessengerClient


class ActionKit:
    def __init__(self, messenger_client: MessengerClient, owner_id: str):
        self.messenger_client = messenger_client
        self.owner_id = owner_id

    def send_message_to_owner(self, message: str) -> None:
        self.messenger_client.send_message(self.owner_id, message)

