from typing import Optional, List

from mbot.bot.action_kit import ActionKit
from mbot.utils.google_apps import GoogleApps

_GOOGLE_APPS_RECORD_TYPES = {
    ("b", "bp"): ("blood_pressure", "blood pressure reading", 3),
    ("h", "hr", "heart"): ("heartrate", "heart rate reading", 1),
    ("j", "jog", "jogging"): ("jogging", "jogging distance reading", 1),
    ("w", "weight"): ("weight", "body weight reading", 1),
    ("p", "press"): ("press", "press workout reading", 3),
    ("t", "temp"): ("temperature", "temperature reading", 1),
    ("f", "food"): ("food", "food", 1),
    ("c", "comment"): ("comment", "comment", 1),
}


class GoogleAppsRecorderFeature:
    def __init__(self, google_apps):
        self.google_apps = google_apps

    def process(self, message: str, action_kit: ActionKit) -> bool:
        tokens = message.split()

        for phrases in _GOOGLE_APPS_RECORD_TYPES:
            item, name, num_fields = _GOOGLE_APPS_RECORD_TYPES[phrases]

            if tokens[0].lower() not in phrases:
                continue

            if len(tokens) < num_fields + 1:
                action_kit.send_message_to_owner(
                    f"Not enough fields given for a {name}."
                )
                return True

            action_kit.send_message_to_owner(f"Saving the {name}...")
            try:
                self.google_apps.record(item, tokens[1:])
                action_kit.send_message_to_owner(f"Successfully saved the {name}!")
            except Exception as e:
                action_kit.send_message_to_owner(
                    f"Error while saving the {name}: {e}"
                )

            return True

        return False
