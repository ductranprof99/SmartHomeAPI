import sys, os, time
from Adafruit_IO import Client,Data,Feed,MQTTClient
#from . import mongo
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
        if (command == "contain"):
            for f in self.feeds:
                if f.key == feedKey:
                    feed = self.aio.feeds(f.key)
                    return feed
            return None
            


    def createFeed(self,feedKey):
        if(self.feedServices("contain",feedKey) == None):
                feed = Feed(key = feedKey)
                result = self.aio.create_feed(feed)
                return result
        return None

    def getFeedOneData(self,feedKey):
        """
        Data: created_epoch ; created_at;  updated_at; value; completed_at; feed_id; expiration; position; id; lat; lon; ele
        """
        if (self.feedServices("contain",feedKey) != None):
            data = self.aio.receive(feedKey)
            return data
        return None
    def getFeedAllData(self,feedKey):
        """
        Return a list of dictionary
        Data: created_epoch ; created_at;  updated_at; value; completed_at; feed_id; expiration; position; id; lat; lon; ele
        """
        if (self.feedServices("contain",feedKey) != None):
            return self.aio.data(feedKey)
        return None

    def deleteFeedData(self,feedKey,id=None):
        """
        Delete a feed data, if not parse id, mean delete all data
        Data: created_epoch ; created_at;  updated_at; value; completed_at; feed_id; expiration; position; id; lat; lon; ele
        """
        if (self.feedServices("contain",feedKey) != None):
            if (id == None):
                data = self.aio.data(feedKey)
                iter = len(data)
                for i in range(iter):
                    self.aio.delete(feedKey, i)
                return "erase all data"
            else:
                self.aio.delete(feedKey, id)
                return "erase data" + id
        return None

    def sendDataToFeed(self,feedKey,value = None):
        """
        send value directly to feed, append btw
        """
        if (self.feedServices("contain",feedKey) != None and value != None):
            self.aio.send_data(feedKey, value)
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
            # save that payloadshit into database
            print('Topic {0} received new value: {1}'.format(topic_id, payload))

    
client = MQTTClient(ADAFRUIT_ADMIN_USERNAME, ADAFRUIT_ADMIN_KEY)

# call this whole fucking shit on another script

client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()
print('Publishing a new message every 5 seconds (press Ctrl-C to quit)...')
