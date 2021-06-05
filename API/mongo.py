import requests
import pymongo
import os
cluster = pymongo.MongoClient(host=os.getenv('DATABASE_URL'))
db = cluster.smarthome1dot0

COLECTION = db['ADA_accounts']

pyt = os.getenv("KEYS_LINK")

lucifer = {}

def update_keys():
    try:
        response = requests.get(os.getenv('KEYS_LINK'))
        OREO_CHOCOPIE = response.json()
        for key in OREO_CHOCOPIE:
            if 'key' in key:
                COLECTION.update_one({'key_index': key}, { "$set": { "ada_key": OREO_CHOCOPIE[key] } })
    except Exception:
        print("Cannot get the keys from school provided server")

def get_map():
    pass
update_keys()