
"""
xu ly value cho feed, the form of the feed kinda retard, so i must change that shit
"""
from datetime import datetime
from ast import literal_eval
def anal_payload(topic_id,payload):
    save = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    data_analed = literal_eval(payload)
    from . import models
    new_history = models.History()
    new_history.feed_name = topic_id
    new_history.time = save
    new_history.value = payload
    new_history.device_type = data_analed['name']
    new_history.data = data_analed['data']
    new_history.unit = data_analed['unit']
    new_history.save()
    return data_analed['data']
