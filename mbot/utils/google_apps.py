import os
import httplib2
import datetime
import sys
import base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleApps:
    def __init__(self, credentials, bp_spreadsheet_id):
        self.bp_spreadsheet_id = bp_spreadsheet_id

        credentials_path = os.path.expanduser("/tmp/.mbot_ga_credentials")
        with open(credentials_path, "w") as f:
            f.write(base64.b64decode(credentials).decode())

        store = Storage(credentials_path)
        self.credentials = store.get()
        if not self.credentials or self.credentials.invalid:
            raise RuntimeError("GoogleApps: Invalid credentials supplied.")

        self.http = self.credentials.authorize(httplib2.Http())

    def record(self, item, values):
        discoveryURL = "https://sheets.googleapis.com/$discovery/rest?version=v4"
        service = discovery.build(
            "sheets", "v4", http=self.http, discoveryServiceUrl=discoveryURL
        )

        total_rows = 3000

        vacant_row = None
        result = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.bp_spreadsheet_id,
                range="Readings!A2:A" + str(total_rows),
            )
            .execute()
        )
        current_values = result.get("values", [])

        if not current_values:
            raise RuntimeError("GoogleApps: Failed to obtain rows in record_bp.")

        if len(current_values) >= total_rows - 1:
            raise RuntimeError("GoogleApps: Table full in record_bp.")

        time_string = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        row_values = [time_string, item] + list(values)
        last_column = chr(ord("A") + len(row_values) - 1)

        vacant_row = 2 + len(current_values)
        update_range = "Readings!A%d:%s%d" % (vacant_row, last_column, vacant_row)
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.bp_spreadsheet_id,
                range=update_range,
                valueInputOption="USER_ENTERED",
                body={"values": [row_values]},
            )
            .execute()
        )
        cells_updated = result.get("updatedCells")

        if cells_updated != len(row_values):
            raise RuntimeError(
                "GoogleApps: Expected {} cells to change"
                " in record_bp, but only {} did.".format(len(row_values), cells_updated)
            )
