
"""
xu ly value cho feed, the form of the feed kinda retard, so i must change that shit
"""
import json
from ast import literal_eval
from datetime import datetime, timedelta,time,date

from pymongo import results
from .mongo import db 

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
    return [data_analed['data'],data_analed['name'],data_analed['unit'],data_analed['id']]


def anal_value(value:str,device_type):
    if device_type == "temperature":
        des = value.split('-')
        return des
    else: return value

        
class Statistic():

    def anal_allDeviceStatistic(self):
        '''
        return list of device's statistic 
        item data form : { device_id, device_type, device_name, phone_number, data_points}
        date format : %d/%m/%Y | type string
        '''
        list_device = list(db['API_device'].find({}))
        queryHistory = list(db['API_history'].find({}))
        queryHistory.sort(key=lambda item:datetime.strptime(item['time'], "%d-%b-%Y (%H:%M:%S.%f)"), reverse=False)
        # need to check type device before make statistic (only for light and fan)
        results = []
        for device in list_device:
            statistic = {}
            if device['device_type'] == 'light' or device['device_type'] == 'fan':
                statistic['device_id'] = str(device['_id'])
                statistic['phone_number'] = device['phone_number']
                statistic['device_name'] = device['device_name']
                statistic['device_type'] = device['device_type']
                statistic['data_points'] = self.anal_DeviceStatistic(queryHistory,str(device['_id']))
                results.append(statistic)
        return results




    def anal_DayRecord(self,listData,previousDay,filterDay):
        '''
        listData format : [{'value','time':dateobject},.....]
        '''
        isOn = previousDay
        previous_time = None
        if isOn:
            timePart = time(0,0,0)
            previous_time = datetime.combine(filterDay,timePart)
        totalTime_1day = timedelta(hours=int(0), minutes=int(0), seconds=float(0))
        for eachStatus in listData:
            if eachStatus['value'] == '0':
                if isOn:
                    deltatime = eachStatus['time'] - previous_time
                    totalTime_1day += deltatime
                    # print(eachStatus['time'])
                    isOn = False    
            else:
                if not isOn:
                    previous_time = eachStatus['time']
                    isOn = True
        res = tuple([{filterDay.strftime("%d/%m/%Y"):(int(totalTime_1day.total_seconds()/36)/100)},isOn])
        return res


    def anal_DeviceStatistic(self,queryHistory,device_id):

        res = []
        listDay_embedDatasInDay = {} # dictionary contain list =  {date: [{value,time}...]}
        for record in queryHistory:
            if record['device_id'] == device_id:
                dateMark = datetime.strptime(record['time'], "%d-%b-%Y (%H:%M:%S.%f)").date()
                if  dateMark in listDay_embedDatasInDay:
                    listDay_embedDatasInDay[dateMark].append({'value':record['value'],'time':datetime.strptime(record['time'], "%d-%b-%Y (%H:%M:%S.%f)")})
                else:
                    listDay_embedDatasInDay[dateMark] = [{'value':record['value'],'time':datetime.strptime(record['time'], "%d-%b-%Y (%H:%M:%S.%f)")}]
            prevDay = False
        for filteredRecord in listDay_embedDatasInDay:
            anal_inserted = self.anal_DayRecord(listDay_embedDatasInDay[filteredRecord],prevDay,filteredRecord)
            res.append(anal_inserted[0])
            prevDay = anal_inserted[1]
        return res


def anal_insertBigOne():
    '''
    update statistic everyday
    '''
    abc = Statistic()
    newStatisTic = abc.anal_allDeviceStatistic();
    for device in newStatisTic:
        db['API_statistic'].update_one({'device_id':device['device_id']},{"$set": device},True)


def anal_insertEveryDay():
    '''
    update statistic everyday
    '''
    abc = Statistic()
    newStatisTic = abc.anal_allDeviceStatistic();
    for device in newStatisTic:
        db['API_statistic'].update_one({'device_id':device['device_id']},{"$set": {'data_points':device['data_points']}},True)