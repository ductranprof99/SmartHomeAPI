import json
from typing import Dict
from Adafruit_IO import Client,Feed,MQTTClient
from datetime import datetime
from .. import analizer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..mongo import db
from API.models import *
from API.serializers import *
import threading

class AdaConnect():
    def __init__(self,username,key):
        self.aio = Client(username,key)
        self.feeds = self.aio.feeds()
        self.groups = self.aio.groups()
    # should try this in try except block

    def feedServices(self,command,feedKey):
        if (command == "delete"):
            self.aio.delete_feed(feedKey)

    def retrievefeedKey(self,feedName):
        for feed in self.feeds:
            if feed.name == feedName:
                return feed.key
        return None

    def contain(self,feedName):
        for feed in self.feeds:
            if feed.name == feedName:
                return True
        return False

    def createFeed(self,feedName):
        if(self.contain(feedName)):
                feed = Feed(name = feedName)
                result = self.aio.create_feed(feed)
                return result
        return None

    def getFeedOneData(self,feedName):
        """
        Data: created_epoch ; created_at;  updated_at; value; completed_at; feed_id; expiration; position; id; lat; lon; ele
        """
        if(self.contain(feedName)):
            feedKey = self.retrievefeedKey(feedName)
            data = self.aio.receive(feedKey)
            return data
        return None
    def getFeedAllData(self,feedName):
        """
        Return a list of dictionary
        Data: created_epoch ; created_at;  updated_at; value; completed_at; feed_id; expiration; position; id; lat; lon; ele
        """
        if(self.contain(feedName)):
            feedKey = self.retrievefeedKey(feedName)
            return self.aio.data(feedKey)
        return None

    def deleteFeedData(self,feedName,id=None):
        """
        Delete a feed data, if not parse id, mean delete all data
        Data: created_epoch ; created_at;  updated_at; value; completed_at; feed_id; expiration; position; id; lat; lon; ele
        """
        if(self.contain(feedName)):
            if (id == None):
                data = self.aio.data(feedName)
                iter = len(data)
                for i in range(iter):
                    self.aio.delete(feedName, i)
                return "erase all data"
            else:
                self.aio.delete(feedName, id)
                return "erase data" + id
        return None

    def sendDataToFeed(self,feedName,value = None):
        """
        send value directly to feed, append btw
        """
        if (self.contain(feedName) and value != None):
            self.aio.send_data(self.retrievefeedKey(feedName), value)
            return "Done"
        return None

def define_on_connected(client: MQTTClient, accesses):
    def on_connected(client: MQTTClient):
        # TODO GET FEED LIST from database (to avoid unnecessary subscription)
        for i in accesses[client._username].feeds:
            print('Listening for changes on user: ' + client._username + "| Feed: " + i.name)
            client.subscribe(i.name)
    return on_connected

def define_on_disconnected():
    def on_disconnected(client):
        print('Disconnected from Adafruit IO!')
    return on_disconnected

def define_on_message(client: MQTTClient, accesses, feedNameToUsername):
    def on_message(client, topic_id, payload):
        save = datetime.datetime.utcnow()
        # find device_id from database, it easier but need to implement later
        device = Device.objects.get(feed_name=topic_id)
        device_serialized = DeviceDetailSerializer(device).data
        phone_number = device_serialized["phone_number"]
        this_home = db['API_home'].find_one({'phone_number':phone_number})
        try:
            status = analizer.anal_payload(topic_id,save,payload,device_serialized["device_id"])  # device_id add later
        except Exception as e:
            print(e)
            print("*** Possibly wrong published message format from adafruit!\n---Payload: " + payload)
            return
        
        # AUTOMATION Mode handling
        if device_serialized["device_type"] == "light_sensor":
            handleLightSensorThead = threading.Thread(target=handleLightSensorAutomation, args=(status[0], device_serialized["phone_number"], accesses, feedNameToUsername))
            handleLightSensorThead.start()
        elif device_serialized["device_type"] == "temperature":
            handleTempSensorThead = threading.Thread(target=handleTemperatureSensorAutomation, args=(status[0], device_serialized["phone_number"], accesses, feedNameToUsername))
            handleTempSensorThead.start()

        # SEND notification to frontend
        if this_home['is_online']:
            context = {'device_id': device_serialized["device_id"] ,'value': status[0]}
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                phone_number,
                {
                    'type': 'send_message_to_frontend',
                    'message': context
                }
            ) 
        
        # UPDATE database
        device.status = status[0]
        device.control_type = status[1]
        device.unit = status[2]
        device.data_id = status[3]
        device.save()

    return on_message    

def handleLightSensorAutomation(sensor_data: str, phone_number: str, accesses: Dict[str, AdaConnect], feedNameToUsername: Dict[str, str]):
    mode = "1" if int(sensor_data) < 100 else "0"
    devices = Device.objects.filter(phone_number=phone_number, device_type="light", automation_mode=2)
    for device in devices:
        data_form = {"id":"","name":"","data":"","unit":""}
        if(device.unit == None):
            data_form["unit"] = ""
        else:  data_form["unit"] = device.unit
        data_form["id"] = device.data_id
        data_form["data"] = mode
        data_form["name"] = device.control_type

        accesses[feedNameToUsername[device.feed_name]].sendDataToFeed(device.feed_name,str(json.dumps(data_form)))

def handleTemperatureSensorAutomation(sensor_data: str, phone_number: str, accesses: Dict[str, AdaConnect], feedNameToUsername: Dict[str, str]):
    temp, humid = [int(data) for data in sensor_data.split("-")]
    mode = "1" if temp > 30 else "0"
    devices = Device.objects.filter(phone_number=phone_number, device_type="fan", automation_mode=2)
    for device in devices:
        # Update (turn on/off) device on adafruit
        data_form = {"id":"","name":"","data":"","unit":""}
        if(device.unit == None):
            data_form["unit"] = ""
        else:  data_form["unit"] = device.unit
        data_form["id"] = device.data_id
        data_form["data"] = mode
        data_form["name"] = device.control_type

        accesses[feedNameToUsername[device.feed_name]].sendDataToFeed(device.feed_name,str(json.dumps(data_form)))