import abc
from typing import Optional, List
from mbot.bot.action_kit import BaseActionKit

from mbot.utils.google_apps import GoogleApps

_GOOGLE_APPS_RECORD_TYPES = {
    ("b", "bp"): ("blood_pressure", "blood pressure reading", 3),
    ("h", "hr", "heart"): ("heartrate", "heart rate reading", 1),
    ("j", "jog", "jogging"): ("jogging", "jogging distance reading", 1),
    ("w", "weight"): ("weight", "body weight reading", 1),
    ("p", "press"): ("press", "press workout reading", 3),
    ("t", "temp"): ("temperature", "temperature reading", 1),
    ("f", "food"): ("food", "food", 1),
    ("c", "comment"): ("comment", "comment", None),
}


class BaseFeature(abc.ABC):
    @abc.abstractmethod
    def process(self, message: str, action_kit: BaseActionKit) -> bool:
        pass


class GoogleAppsRecorderFeature(BaseFeature):
    def __init__(self, google_apps):
        self.google_apps = google_apps

    def process(self, message: str, action_kit: BaseActionKit) -> bool:
        tokens = message.split()

        for phrases in _GOOGLE_APPS_RECORD_TYPES:
            item, name, num_fields = _GOOGLE_APPS_RECORD_TYPES[phrases]

            if tokens[0].lower() not in phrases:
                continue

            # If num_fields is None, treat everything after the first token as a single field
            if num_fields is None:
                if len(tokens) < 2:
                    action_kit.send_message_to_owner(
                        f"Not enough fields given for a {name}."
                    )
                    return True
                
                # Join all tokens after the first one as a single string
                values = [" ".join(tokens[1:])]
            else:
                if len(tokens) < num_fields + 1:
                    action_kit.send_message_to_owner(
                        f"Not enough fields given for a {name}."
                    )
                    return True
                
                values = tokens[1:]

            action_kit.send_message_to_owner(f"Saving the {name}...")
            try:
                self.google_apps.record(item, values)
                action_kit.send_message_to_owner(f"Successfully saved the {name}!")
            except Exception as e:
                action_kit.send_message_to_owner(f"Error while saving the {name}: {e}")

            return True

        return False
