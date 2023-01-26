# tempsensor_balena

Balena image for Raspberry Pi 3.

Reads temperature data from RTL-SDR via RT_433 from a Clas Ohlson temperature / humidity sensor (e.g https://www.clasohlson.com/no/Temperaturgiver---hygrometer/p/36-6726 or other devices using the same protocol), as well as from a Netatmo outdoor sensor via API. Data is uploaded to an InfluxDB bucket for tracking purposes. 
Optionally adds an extra indoor sensor
All configuration needs to be set as Balenda device variables:

* INFLUXDB_ORG
* INFLUXDB_SENSOR_BUCKET
* INFLUXDB_TOKEN
* NETATMO_CLIENT_ID
* NETATMO_CLIENT_SECRET
* NETATMO_PASSWORD
* NETATMO_USER
* OUTDOOR_SENSOR_ID
