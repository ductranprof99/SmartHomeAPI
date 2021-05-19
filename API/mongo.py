# from os import error
# import bson
# import  pymongo
# client  = pymongo.MongoClient("mongodb+srv://Hao:khongco@cluster0.zx05d.mongodb.net/smarthome1dot0?retryWrites=true&w=majority")
# db = client.smarthome1dot0


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