from os import error
import bson
import  pymongo
from collections import namedtuple
client  = pymongo.MongoClient("mongodb+srv://Hao:khongco@cluster0.zx05d.mongodb.net/smarthome1dot0?retryWrites=true&w=majority")
db = client.smarthome1dot0
history_table = db['API_device_history']
device_table = db['API_deviceadmin']


DEVICE_HISTORY_FORM = ['phone_number','feed-id','type','value','time']
DEVICE_FORM = ['phone-number','inhouse_id','feed-name','type','status','create-time']
history_data = namedtuple('history_data',DEVICE_HISTORY_FORM)




class History:
    '''
        do something with history of device
    '''
    def insert(self,name,value,time):
        similar = device_table.find_one({'feed-name':name},{'_id':1,'phone-number':1,'inhouse-id':0,'feed-name':0,'type':1,'status':0,'create-time':0})
        data_input = dict(history_data(similar['phone-number'],similar['_id'],similar['type'],value,time)._asdict())
        try:
            history_table.insert_one(data_input)
            return 1
        except(Exception):
            return 0

    def update(self,name,value,time):
        myquery = { "feed-name": name, 'time': time}
        newvalues = { "$set": { "value": value } }

        history_table.update_one(myquery, newvalues)

        try:
            x = history_table.update_one(myquery,newvalues)
            return x
        except(Exception):
            return None
    def delete_all(self):
        '''
        admin control, drop then recreate
        '''
        try:
            history_table.drop()
            history_table = db['API_device_history']
            return 1
        except(Exception):
            return 0
    def delete_1_in_1_device(self,name,time):
        '''
        admin and user can control, delete 1 row
        '''
        try:
            myquery = { "feed-name": name, 'time': time}
            history_table.delete_one(myquery)
            return 1
        except(Exception):
            return None


    def delete_all_in_1_device(self,name):
        '''
        admin and user can control, delete all history row in 1 device
        '''
        try:
            myquery = { "feed-name": name}
            history_table.delete_many(myquery)
            return 1
        except(Exception):
            return None



class Device_admin:
    '''
    do something with history of device
    '''
    def insert(self,name,value,time):
        similar = device_table.find_one({'feed-name':name},{'_id':1,'phone-number':1,'inhouse-id':0,'feed-name':0,'type':1,'status':0,'create-time':0})
        data_input = dict(history_data(similar['phone-number'],similar['_id'],similar['type'],value,time)._asdict())
        try:
            history_table.insert_one(data_input)
            return 1
        except(Exception):
            return 0

    def update(self,name,value,time):
        myquery = { "feed-name": name, 'time': time}
        newvalues = { "$set": { "value": value } }

        history_table.update_one(myquery, newvalues)

        try:
            x = history_table.update_one(myquery,newvalues)
            return x
        except(Exception):
            return None
    def delete_all(self):
        '''
        admin control, drop then recreate
        '''
        try:
            history_table.drop()
            history_table = db['API_device_history']
            return 1
        except(Exception):
            return 0
    def delete_1_in_1_device(self,name,time):
        '''
        admin and user can control, delete 1 row
        '''
        try:
            myquery = { "feed-name": name, 'time': time}
            history_table.delete_one(myquery)
            return 1
        except(Exception):
            return None


    def delete_all_in_1_device(self,name):
        '''
        admin and user can control, delete all history row in 1 device
        '''
        try:
            myquery = { "feed-name": name}
            history_table.delete_many(myquery)
            return 1
        except(Exception):
            return None

# convert to dictionary input = dict(history_data(...,...,...,...,...)._asdict())

# class Devicecontrol:
#     """
#     feed id auto generate by adafruit
#     """
#     ##Khoi tao gia tri mac dinh cho house
#     def __init__(self):
#         self.error="none"
#         self.mycollection= db['API_deviceadmin']
#         self.id= "unknown"
#         self.data={
# 	    "name": "noname",
#         "house": "unknow",
# 	    "key":	"unknown",
# 	    "description":"unset",
# 	    "devicetype": "unknown",
# 	    "status":	"unknown",
#         }
#     ##Cac phuong thuc get du lieu
#     def getid(self): return self.id
#     def getname(self): return self.data["name"]
#     def gethouse(self): return self.data["house"]
#     def getkey(self): return self.data["key"]
#     def getdescription(self): return self.data["description"]
#     def getdevicetype(self): return self.data["devicetype"]
#     def getstatus(self): return self.data["status"]
#     ##Get error
#     def geteror(self):
#         return self.error
#     ##Cac phuong thuc protected
#     def checkdevice_unique(self,feedkey):
#         tmp=list(self.mycollection.find({"key":feedkey}))
#         if(len(tmp)==0):
#             return False
#         else:
#             return True
#     def checkdevice_house(self,house):
#         tmp=list(self.mycollection.find({"house":house}))
#         if(len(tmp)==0):
#             return False
#         else:
#             return tmp
#     ##insert vao csdl
#     def insert(self, name , key , house , description, devicetype, status):
#         if(not(self.checkdevice_unique(key))):
#             self.data["name"]=str(name)
#             self.data["key"]=str(key)
#             self.data["house"]=str(house)
#             self.data["description"]=str(description)
#             self.data["devicetype"]=str(devicetype)
#             self.data["status"]=str(status)
#             tmp=self.mycollection.insert_one(self.data)
#             self.id=tmp.inserted_id
#             self.error="none"
#             return True
#         else:
#             self.error="feed had been inserted"
#             return False
#     ##get info feed id
#     def getbyfeedid(self, feedkey):
#         if(not(self.checkdevice_unique(feedkey))):
#             self.error="feed unknow"
#             return False
#         else:
#             tmp=self.mycollection.find({"key":feedkey})
#             self.id=tmp[0]["_id"]
#             self.data["name"]= tmp[0]["name"] 
#             self.data["key"]= feedkey
#             self.data["house"]= tmp[0]["house"] 
#             self.data["description"] = tmp[0]["description"]
#             self.data["devicetype"] = tmp[0]["devicetype"] 
#             self.data["status"] = tmp[0]["status"] 
#             self.error="none"
#             return True

#     def update_one(self,feedKey,dictKey,value):
#         if(not(self.getbyfeedid(feedKey))):
#             self.error="feed unknow"
#             return False
#         else:
#             filter = {"key" : feedKey}
#             newvalues = { "$set": { str(dictKey): value } }
#             self.mycollection.update_one(filter,newvalues)
#             return True
#     def delete_one(self,feedKey):
#         pass
# # a=House()
# # print(a.getbyphonenum("0346148097"))
# # print(a.geteror())
# # print(a.getid())
# # print(type(bson.ObjectId( "123123123123123123123123")))
# print(db["__schema__"].find_many().limit(10))