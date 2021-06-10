from . import adafruit
from .. import mongo
from ..mongo import db
from Adafruit_IO import MQTTClient
import os

mongo.update_keys()

list_account = db['ADA_accounts']
all_ada_usernames = list(list_account.find({},{"_id":0, "key_index": 0 }))
accesses = {}
mqttClients = {}
feedNameToUsername = {}

for account in all_ada_usernames:
    if "CSE_BBC" in account['user_name']:
        continue
    user_name = account['user_name']
    ada_key = account['ada_key']
    try:
        accesses[user_name] = adafruit.AdaConnect(user_name, ada_key)
        for feed in accesses[user_name].feeds:
            feedNameToUsername[feed.name] = user_name
        mqttClients[user_name] = MQTTClient(user_name, ada_key)
    except:
        print("Cannot connect to adafruitIO user: " + user_name)

def Listen():
    for client_ in mqttClients:
        client = mqttClients[client_]
        client.on_connect    = adafruit.define_on_connected(client=client, accesses=accesses)
        client.on_disconnect = adafruit.define_on_disconnected()
        client.on_message    = adafruit.define_on_message(client=client, accesses=accesses, feedNameToUsername=feedNameToUsername)
        client.connect()
        mqttClients[client_].loop_background()

if os.getenv("ADA_LISTEN") == 'False':
    pass
else:
    Listen()