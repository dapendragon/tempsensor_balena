import json
import fileinput
import influxdb_client, os, requests
from NetatmoCreds import NetatmoCreds
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

netatmoCreds = NetatmoCreds()

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = "https://europe-west1-1.gcp.cloud2.influxdata.com"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org, timeout=os.environ.get("INFLUXDB_TIMEOUT"))
bucket = os.environ.get("INFLUXDB_SENSOR_BUCKET")

write_api = client.write_api(write_options=SYNCHRONOUS)


def fetch_netatmo_data():
    netatmoCreds.refresh()
    headers = {
        "Authorization": "Bearer " + netatmoCreds.accessToken,
        "accept": "application/json"
    }

    r = requests.get("https://api.netatmo.com/api/getstationsdata?get_favorites=false", headers=headers)
    response = r.json()

    modules = response["body"]["devices"][0]["modules"]
    for module in modules:
        if module["module_name"] == "Tempmåler ute":
            netatmo_data = {
                "temp": module["dashboard_data"]["Temperature"],
                "humidity": module["dashboard_data"]["Humidity"]
            }
            return netatmo_data


for line in fileinput.input():
    data = json.loads(line.rstrip())
    netatmo_data = fetch_netatmo_data()

    influx_packet = [
        Point("weather_data")
        .field("temperature", data["temperature_C"])
        .field("humidity", data["humidity"])
        .tag("source", "SDR"),

        Point("netatmo_data")
        .field("temperature", netatmo_data["temp"])
        .field("humidity", netatmo_data["humidity"])
        .tag("source", "Netatmo"),
    ]

    write_api.write(bucket=bucket, org=os.environ.get("INFLUXDB_ORG"), record=influx_packet)
