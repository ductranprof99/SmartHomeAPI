import sys, os
from Adafruit_IO import Client,Data,Feed,MQTTClient
ADAFRUIT_ADMIN_USERNAME = os.getenv("ADAFRUIT_ADMIN_USERNAME") 
ADAFRUIT_ADMIN_KEY = os.getenv("ADAFRUIT_IO_KEY") 
class AdaConnect():
    def __init__(self,username,key):
        self.aio = Client(username,key)
        self.feeds = self.aio.feeds()

    # should try this in try except block
    def feedServices(self,command,feedName):
        if (command == "delete"):
            self.aio.delete_feed(feedName)
        if (command == "contain"):
            for f in self.feeds:
                if f.name == feedName:
                    feed = self.aio.feeds(f.name)
                    return feed
            return None
        if (command == "create"):
            if(self.feedServices("contain",feedName) == None):
                feed = Feed(name = feedName)
                result = self.aio.create_feed(feed)
                return result

    def dataServices(self,serviceName,name = '',message = None,id = None):
        if (self.feedServices("contain",name) != None):
            if(serviceName == 'receive'):
                    data = self.aio.receive(name)
                    temp = int(data.value)
                    return temp
            if(serviceName == 'send'):
                #  append a new value to a feed
                test = self.aio.feeds(name)
                if(message != None):
                    self.aio.send_data(test.key, message)
                else:
                    return 'Null message'
            if(serviceName =='get all'):
                # get all of the data for a feed by using retrieve, return list type
                return self.aio.data(name)
            if(serviceName == 'delete'):
                if (id == None):
                    data = self.aio.data(name)
                    iter = len(data)
                    for i in range(iter):
                        self.aio.delete(name, i)
                    return "erase all data"
                else:
                    self.aio.delete(name, id)
                    return "erase data" + id
        else:
            return 'Doesn\'t have that feed'

class AdaSubLive():

    def __init__(self,feedName):
        self.FEED_ID = feedName
    def connected(self,client):
        
        print('Connected to Adafruit IO!  Listening for {0} changes...'.format(self.FEED_ID))
        client.subscribe(self.FEED_ID)

    def subscribe(self,client, userdata, mid, granted_qos):
        # This method is called when the client subscribes to a new feed.
        print('Subscribed to {0} with QoS {1}'.format(self.FEED_ID, granted_qos[0]))

    def disconnected(self,client):
        # Disconnected function will be called when the client disconnects.
        print('Disconnected from Adafruit IO!')
        sys.exit(1)

    def message(self,client, feed_id, payload):
        # Message function will be called when a subscribed feed has a new value.
        # The feed_id parameter identifies the feed, and the payload parameter has
        # the new value.
        print('Feed {0} received new value: {1}'.format(feed_id, payload))

    def start(self,username,key):
        # using this method to start listening the feed
        # not tested yet, my idea to using loop_background so i can call this services within 
        # django server
        client = MQTTClient(username,key)
        client.on_connect    = self.connected
        client.on_disconnect = self.disconnected
        client.on_message    = self.message
        client.on_subscribe  = self.subscribe
        client.connect()
        client.loop_background()

access = AdaConnect(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)