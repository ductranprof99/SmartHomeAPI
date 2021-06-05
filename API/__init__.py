from Adafruit_IO import client
from . import mqtt
from . import mongo

mongo.update_keys()

for client_ in mqtt.mqttClients:
    mqtt.mqttClients[client_].loop_background()