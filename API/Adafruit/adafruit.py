from Adafruit_IO import Client,Feed,MQTTClient
from datetime import datetime
from .. import analizer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..mongo import db

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

def define_on_message(client: MQTTClient):
    def on_message(client, topic_id, payload):
        # TODO REMOVE & FIX this ugly feed_name_array
        save = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        # find device_id from database, it easier but need to implement later
        device = db['API_device'].find_one({'feed_name':topic_id})
        if device != None:
            phone_number = db['API_device'].find_one({'feed_name':topic_id})['phone_number'] 
            this_home = db['API_home'].find_one({'phone_number':phone_number})
            try:
                status = analizer.anal_payload(topic_id,save,payload,device['device_id'])  # device_id add later
            except:
                print("*** Possibly wrong published message format from adafruit!\n---Payload: " + payload)
                return
            if this_home['is_online']:
                list_device = this_home['devices']
                a = 1
                for i in list_device:
                    if i['device_id'] == device['device_id']:
                        break;
                    a+=1
                context = {'device_id': a ,'value': status[0]}
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    phone_number,
                    {
                        'type': 'send_message_to_frontend',
                        'message': context
                    }
                ) 
            db['API_device'].update_one({ "feed_name": topic_id },{ "$set": { "status": status[0] ,'control_type':status[1],'unit':status[2],'data_id':status[3]} })
        print(payload)
    return on_message