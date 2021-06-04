from Adafruit_IO import Client,Feed,MQTTClient
from datetime import datetime
import sys, os
from . import analizer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .mongo import db


list_account = db['ADA_accounts']


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


LIST_ACCOUNT_QUERIED = list(list_account.find({},{"_id":0, "key_index": 0 }))


try:
    ACESS = [AdaConnect(ACCOUNT['user_name'], ACCOUNT['ada_key']) for ACCOUNT in LIST_ACCOUNT_QUERIED]
except Exception:
    print('cannot connect')
feed_name_array = []

for i in range(len(LIST_ACCOUNT_QUERIED)):
    feed_name_array += [c.name for c in ACESS[i].feeds]


def connected(client):
    print('Listening for changes on all shit')
    for i in feed_name_array:
        client.subscribe(i)
def disconnected(client):
    print('Disconnected from Adafruit IO!')
def message(client, topic_id, payload):
    for feed_id in feed_name_array:
        if topic_id == feed_id:
            save = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            # find device_id from database, it easier but need to implement later
            device = db['API_device'].find_one({'feed_name':topic_id})
            if device != None:
                phone_number = db['API_device'].find_one({'feed_name':topic_id})['phone_number'] 
                this_home = db['API_home'].find_one({'phone_number':phone_number})
                status = analizer.anal_payload(topic_id,save,payload,device['device_id'])  # device_id add later
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


# this things for multiple account
# clients = [MQTTClient(ACCOUNT['user_name'], ACCOUNT['ada_key']) for ACCOUNT in LIST_ACCOUNT_QUERIED]

# for test server 
clients = [MQTTClient(LIST_ACCOUNT_QUERIED[2]['user_name'], LIST_ACCOUNT_QUERIED[2]['ada_key'])]
# call loop fucking shit on another script
for client in clients:
    client.on_connect    = connected
    client.on_disconnect = disconnected
    client.on_message    = message
    client.connect()
    print('///////////// pre check modify hehehehehehee /////////////////')
print('Publishing a new message every 40 seconds (press Ctrl-C to quit)...')
