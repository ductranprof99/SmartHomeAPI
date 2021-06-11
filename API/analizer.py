
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


    def calculate(self,phonenumber,week=None,month=None,type_dev=None):
        lt = datetime.now()
        if week != None:
            self.deltaday = 7*week
            d = timedelta(days = 7*week)
            gt = lt - d
            return self.combine(phonenumber,gt,lt,type_dev)
        else:
            self.deltaday = 30*month
            d = timedelta(days = 30*month)
            gt = lt - d
            return self.combine(phonenumber,gt,lt,type_dev)

    def combine(self,phonenumber,gt,lt,type_dev):
        self.devices = list(db['API_device'].find({'phone_number':phonenumber}))
        res = {}
        if(type_dev == 'light'):
            list_light = [{'id':str(a_dict['_id']),'device_name':a_dict['device_name']} for a_dict in self.devices if a_dict['device_type'] == 'light']
            list_type = [a_dict['id'] for a_dict in list_light]
            lights_his = []
            for deviceid in list_type:
                a = list(db['API_history'].find({"$and": [{"time": {'$gt': gt,'$lte':lt }},{'device_id':deviceid}]}))
                lights_his += a
            res.update({'light':self.anal_lightStatistic(list_light,lights_his)})
        elif(type_dev == 'fan'):
            list_fan =  [{'id':str(a_dict['_id']),'device_name':a_dict['device_name']} for a_dict in self.devices if a_dict['device_type'] == 'fan']
            list_type = [a_dict['id'] for a_dict in list_fan]
            fans_his = []
            for deviceid in list_type:
                a = list(db['API_history'].find({"$and": [{"time": {'$gt': gt,'$lte':lt }},{'device_id':deviceid}]}))
                fans_his += a
            res.update({'fan':self.anal_fanStatistic(list_fan,fans_his)})
        return res

    def anal_lightStatistic(self,list_light,lights_his):
        list_statistic = self.anal_DeviceSameType(list_light,lights_his)
        light_dict = {'total': 0,'day_average':0,'data_points':{},'device_usage': []}
        for device in list_statistic:
            light_dict['total']+= device['total']
            light_dict['device_usage'].append({'device_name':device['device_name'],'total':device['total']})
            for i in device['data_points']:
                if i.strftime("%d/%m/%Y") in light_dict['data_points']:
                    light_dict['data_points'][i.strftime("%d/%m/%Y")] += device['data_points'][i]
                else:  light_dict['data_points'][i.strftime("%d/%m/%Y")] = device['data_points'][i]
        light_dict['day_average'] = light_dict['total']/self.deltaday
        return light_dict

    def anal_fanStatistic(self,list_fan,fans_his):
        list_statistic = self.anal_DeviceSameType(list_fan,fans_his)
        fan_dict = {'total': 0,'day_average':0,'data_points':{},'device_usage': []}
        for device in list_statistic:
            fan_dict['total']+= device['total']
            fan_dict['device_usage'].append({'device_name':device['device_name'],'total':device['total']})
            for i in device['data_points']:
                if i.strftime("%d/%m/%Y") in fan_dict['data_points']:
                    fan_dict['data_points'][i.strftime("%d/%m/%Y")] += device['data_points'][i]
                else:  fan_dict['data_points'][i.strftime("%d/%m/%Y")] = device['data_points'][i]
        fan_dict['day_average']+= fan_dict['total']/self.deltaday
        return fan_dict


    def anal_DeviceSameType(self,list_device,queryHistory):
        '''
        return list of device's statistic 
        item data form : { device_id, device_name, data_points,total}
        date format : %d/%m/%Y | type string
        '''
        results = []
        for device in list_device:
            statistic = {}
            statistic['device_id'] = device['id']
            statistic['device_name'] = device['device_name']
            statistic['data_points'] = self.anal_DeviceStatistic(queryHistory,device['id'])
            total = 0
            for day in statistic['data_points'].items():
                total += day[1]
            statistic['total'] = total
            results.append(statistic)
        return results




    def anal_DayRecord(self,listData,previousDay,filterDay):
        '''
        listData format : [{'value','time':dateobject},.....]
        '''
        isOn = previousDay
        previous_time = None
        end_day = datetime.combine(filterDay,time=time(23,59,59))
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
        if(isOn):
            deltatime = end_day - previous_time
            totalTime_1day += deltatime
        res = tuple([{filterDay:(int(totalTime_1day.total_seconds()/36)/100)},isOn])  #filterday is date object (only date)
        return res


    def anal_DeviceStatistic(self,queryHistory,device_id):

        res = {}
        listDay_embedDatasInDay = {} # dictionary contain list =  {date: [{value,time}...]}
        for record in list(queryHistory):
            if record['device_id'] == device_id:
                dateMark = record['time'].date()
                if  dateMark in listDay_embedDatasInDay:
                    listDay_embedDatasInDay[dateMark].append({'value':record['value'],'time':record['time']})
                else:
                    listDay_embedDatasInDay[dateMark] = [{'value':record['value'],'time':record['time']}]
        prevDay = False
        for filteredRecord in listDay_embedDatasInDay:
            anal_inserted = self.anal_DayRecord(listDay_embedDatasInDay[filteredRecord],prevDay,filteredRecord)
            res.update(anal_inserted[0])
            prevDay = anal_inserted[1]
        return res

