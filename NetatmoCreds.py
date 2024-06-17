import requests
import os, logging, traceback
from datetime import datetime, timedelta


class NetatmoCreds:
    accessToken = ""
    refreshToken = os.environ.get("NETATMO_REFRESH_TOKEN")
    timeLimit = datetime.now()

    def refresh(self):

        if self.accessToken == "" or datetime.now() > self.timeLimit:
            auth_payload = {
                "client_id": os.environ.get("NETATMO_CLIENT_ID"),
                "client_secret": os.environ.get("NETATMO_CLIENT_SECRET"),
                "grant_type": "refresh_token",
                "refresh_token": self.refreshToken
            }
            self.fetchcreds(auth_payload)

    def fetchcreds(self, auth_payload):
        auth_url = "https://api.netatmo.com/oauth2/token"
        try:
            r = requests.post(auth_url, data=auth_payload)
            response = r.json()
            self.accessToken = response["access_token"]
            self.refreshToken = response["refresh_token"]
            self.timeLimit = datetime.now() + timedelta(seconds=response["expires_in"])
            print("New access tokens expire at " + str(self.timeLimit))
        except Exception as e:
            logging.error(traceback.format_exc())
