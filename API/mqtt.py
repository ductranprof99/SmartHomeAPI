from Adafruit_IO import Client,Data,Feed,MQTTClient
from datetime import datetime
import sys, os
import pymongo
from . import analizer
cluster = pymongo.MongoClient(host=os.getenv('DATABASE_URL'))
db = cluster.smarthome1dot0
ADAFRUIT_ADMIN_USERNAME = os.getenv('ADAFRUIT_ADMIN_USERNAME')
ADAFRUIT_ADMIN_KEY = os.getenv('ADAFRUIT_IO_KEY')
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


access = AdaConnect(ADAFRUIT_ADMIN_USERNAME, ADAFRUIT_ADMIN_KEY)
feed_name_array = [i.name for i in access.feeds]


def connected(client):
    print('Listening for changes on all shit')
    for i in feed_name_array:
        client.subscribe(i)

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, topic_id, payload):
    for feed_id in feed_name_array:
        if topic_id == feed_id:
            save = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            # find device_id from database, it easier but need to implement later
            # device_id = db['API_device'].find_one({'feed_name':topic_id})['device_id'] 
            status = analizer.anal_payload(topic_id,save,payload,'device_id')  # device_id add later
            db['API_device'].update_one({ "feed_name": topic_id },{ "$set": { "status": status } })
            print(payload)


    
client = MQTTClient(ADAFRUIT_ADMIN_USERNAME, ADAFRUIT_ADMIN_KEY)

# call this whole fucking shit on another script

client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()
print('Publishing a new message every 5 seconds (press Ctrl-C to quit)...')
