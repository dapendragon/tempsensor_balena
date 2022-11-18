import requests
import os
from datetime import datetime, timedelta


class NetatmoCreds:
    accessToken = ""
    refreshToken = ""
    timeLimit = datetime.now()

    def refresh(self):
        if datetime.now() > self.timeLimit and self.refreshToken == "":
            print("Fetching new OAuth tokens...")
            auth_payload = {
                "client_id": os.environ.get("NETATMO_CLIENT_ID"),
                "client_secret": os.environ.get("NETATMO_CLIENT_SECRET"),
                "grant_type": "password",
                "username": os.environ.get("NETATMO_USER"),
                "password": os.environ.get("NETATMO_PASSWORD"),

            }
            self.fetchcreds(auth_payload)

        elif datetime.now() > self.timeLimit:
            auth_payload = {
                "client_id": os.environ.get("NETATMO_CLIENT_ID"),
                "client_secret": os.environ.get("NETATMO_CLIENT_SECRET"),
                "grant_type": "refresh_token",
                "refresh_token": self.refreshToken
            }
            self.fetchcreds(auth_payload)

    def fetchcreds(self, auth_payload):
        auth_url = "https://api.netatmo.com/oauth2/token"
        r = requests.post(auth_url, data=auth_payload)
        response = r.json()
        self.accessToken = response["access_token"]
        self.refreshToken = response["refresh_token"]
        self.timeLimit = datetime.now() + timedelta(seconds=response["expires_in"])
        print("New access tokens expire at " + str(self.timeLimit))
