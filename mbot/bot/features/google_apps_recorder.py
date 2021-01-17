from typing import Optional, List

from mbot.bot.action_kit import ActionKit
from mbot.utils.google_apps import GoogleApps

_GOOGLE_APPS_RECORD_TYPES = {
    ("b", "bp"): ("blood_pressure", "blood pressure reading", 4),
    ("h", "hr", "heart"): ("heartrate", "heart rate reading", 1),
    ("j", "jog", "jogging"): ("jogging", "jogging distance", 1),
    ("w", "weight"): ("weight", "body weight", 1),
    ("p", "press"): ("press", "press workout", 3),
    ("ot", "otemp"): ("oral_temperature", "oral temperature reading", 1),
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

            action_kit.send_message_to_owner(f"Recording your {name}...")
            try:
                self.google_apps.record(item, tokens[1 : num_fields + 1])
                action_kit.send_message_to_owner(f"Successfully recorded your {name}!")
            except Exception as e:
                action_kit.send_message_to_owner(
                    f"Error while recording your {name}: {e}"
                )

            return True

        return False

