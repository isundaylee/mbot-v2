import abc
from mbot.utils.messenger import MessengerClient
import slack_sdk


class BaseActionKit(abc.ABC):
    @abc.abstractmethod
    def send_message_to_owner(self, message: str) -> None:
        pass


class MessengerActionKit(BaseActionKit):
    def __init__(self, messenger_client: MessengerClient, owner_id: str):
        self.messenger_client = messenger_client
        self.owner_id = owner_id

    def send_message_to_owner(self, message: str) -> None:
        self.messenger_client.send_message(self.owner_id, message)


class SlackActionKit(BaseActionKit):
    def __init__(
        self, slack_client: slack_sdk.WebClient, channel_id: str, thread_ts: str
    ):
        self._slack_client = slack_client
        self._channel_id = channel_id
        self._thread_ts = thread_ts

    def send_message_to_owner(self, message: str) -> None:
        self._slack_client.chat_postMessage(
            channel=self._channel_id, thread_ts=self._thread_ts, text=message
        )
