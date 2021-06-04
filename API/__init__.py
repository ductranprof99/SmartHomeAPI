from Adafruit_IO import client
from . import mqtt
from . import mongo

mongo.update_keys()

for i in mqtt.clients:
    i.loop_background()