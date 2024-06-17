import json
import fileinput
import os, requests, logging, traceback
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from NetatmoCreds import NetatmoCreds
from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision, WriteOptions

netatmoCreds = NetatmoCreds()

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_URL")

client = InfluxDBClient3(host=url, token=token, org=org, timeout=20000)
bucket = os.environ.get("INFLUXDB_SENSOR_BUCKET")


def fetch_netatmo_data():
    netatmoCreds.refresh()
    headers = {
        "Authorization": "Bearer " + netatmoCreds.accessToken,
        "accept": "application/json"
    }
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    try:

        r = session.get("https://api.netatmo.com/api/getstationsdata?get_favorites=false", headers=headers)
        response = r.json()
        modules = response["body"]["devices"][0]["modules"]
        for module in modules:
            if module["module_name"] == "Tempmåler ute":
                netatmo_data = {
                    "temp": module["dashboard_data"]["Temperature"],
                    "humidity": module["dashboard_data"]["Humidity"]
                }
                return netatmo_data
    except Exception as e:
        logging.error(traceback.format_exc())



for line in fileinput.input():
    data = json.loads(line.rstrip())
    outside = data['id'] == int(os.environ.get("OUTDOOR_SENSOR_ID"))
    sdr_desc = "weather_data"
    sdr_source = "SDR"

    if not outside:
        sdr_desc = "filament_data"
        sdr_source = "indoor_SDR"

    influx_packet = [
        Point(sdr_desc)
        .field("temperature", float(data["temperature_C"]))
        .field("humidity", float(data["humidity"]))
        .tag("source", sdr_source)
    ]

    if outside:
        netatmo_data = fetch_netatmo_data()
        influx_packet.append(
            Point("netatmo_data")
            .field("temperature", float(netatmo_data["temp"]))
            .field("humidity", float(netatmo_data["humidity"]))
            .tag("source", "Netatmo")
        )
    try:
        client.write(database=bucket, record=influx_packet)
    except Exception as e:
        print("Read timeout sending data to InfluxDB")
        logging.error(traceback.format_exc())
