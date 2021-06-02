
"""
xu ly value cho feed, the form of the feed kinda retard, so i must change that shit
"""

from ast import literal_eval
def anal_payload(topic_id,time,payload,device_id):
    data_analed = literal_eval(payload)
    from . import models
    new_history = models.History()
    new_history.feed_name = topic_id
    new_history.device_id = device_id
    new_history.time = time
    new_history.value = data_analed['data']
    new_history.device_type = data_analed['name']
    new_history.unit = data_analed['unit']
    new_history.save()
    return [data_analed['data'],data_analed['name'],data_analed['unit']]


def anal_value(value:str,device_type):
    if device_type == "temperature":
        des = value.split('-')
        return des
    else: return value