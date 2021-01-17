from mbot.messenger import MessengerClient


class Bot:
    def __init__(self, features, messenger_client: MessengerClient, owner_id):
        self.features = features
        self.messenger_client = messenger_client
        self.owner_id = owner_id

    def process_message(self, message: str) -> None:
        for feature in self.features:
            responses = feature.process(message)
            if responses is None:
                continue

            for response in responses:
                self.messenger_client.send_message(self.owner_id, response)
            return

        self.messenger_client.send_message(
            self.owner_id, "Sorry, I don't understand ):"
        )

