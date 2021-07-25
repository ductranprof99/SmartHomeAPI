
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
        self.lt = datetime.now()
        self.today = self.lt.date()
        if week != None:
            self.deltaday = 7*week
            d = timedelta(days = 7*week)
            self.gt = self.lt - d
            return self.combine(phonenumber,self.gt,self.lt,type_dev)
        else:
            self.deltaday = 30*month
            d = timedelta(days = 30*month)
            self.gt = self.lt - d
            return self.combine(phonenumber,self.gt,self.lt,type_dev)


    def combine(self,phonenumber,gt,lt,type_dev):
        self.type_dev = type_dev
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
        elif(type_dev == 'temperature'):
            list_temperature =  [{'id':str(a_dict['_id']),'device_name':a_dict['device_name']} for a_dict in self.devices if a_dict['device_type'] == 'temperature']
            list_type = [a_dict['id'] for a_dict in list_temperature]
            fans_his = []
            for deviceid in list_type:
                a = list(db['API_history'].find({"$and": [{"time": {'$gt': gt,'$lte':lt }},{'device_id':deviceid}]}))
                fans_his += a
            res.update({'temperature':self.anal_tempStatistic(list_temperature,fans_his)})
        return res

    def anal_lightStatistic(self,list_light,lights_his):
        list_statistic = self.anal_DeviceSameTypeFanLight(list_light,lights_his)
        light_dict = {'total': 0,'day_average':0,'data_points':{},'device_usage': []}
        for device in list_statistic:
            light_dict['total']+= device['total']
            light_dict['device_usage'].append({'device_name':device['device_name'],'total':device['total'],'isOverUsed':device['mean']})
            for i in device['data_points']:
                if i.strftime("%d/%m/%Y") in light_dict['data_points']:
                    light_dict['data_points'][i.strftime("%d/%m/%Y")] += device['data_points'][i]
                else:  light_dict['data_points'][i.strftime("%d/%m/%Y")] = device['data_points'][i]
        light_dict['day_average'] = light_dict['total']/self.deltaday
        return light_dict

    def anal_fanStatistic(self,list_fan,fans_his):
        list_statistic = self.anal_DeviceSameTypeFanLight(list_fan,fans_his)
        fan_dict = {'total': 0,'day_average':0,'data_points':{},'device_usage': []}
        for device in list_statistic:
            fan_dict['total']+= device['total']
            fan_dict['device_usage'].append({'device_name':device['device_name'],'total':device['total'],'isOverUsed':device['mean']})
            for i in device['data_points']:
                if i.strftime("%d/%m/%Y") in fan_dict['data_points']:
                    fan_dict['data_points'][i.strftime("%d/%m/%Y")] += device['data_points'][i]
                else:  fan_dict['data_points'][i.strftime("%d/%m/%Y")] = device['data_points'][i]
        fan_dict['day_average']+= fan_dict['total']/self.deltaday
        return fan_dict

    def anal_tempStatistic(self,list_device,queryHistory):
        '''
        return list of temperature and humid sensor type device's statistic 
        item data form : { device_id, device_name, data_points}
        date format : %d/%m/%Y | type string
        '''
        results = []
        for device in list_device:
            statistic = {}
            statistic['data_points'] = self.anal_DeviceStatistic(queryHistory,device['id'])
            statistic['device_usage'] = {"device_name": device['device_name']}
            results.append(statistic)
        return results
        
    


    def anal_DeviceSameTypeFanLight(self,list_device,queryHistory):
        '''
        return list of light or fan type device's statistic 
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
            statistic['mean'] = total/self.deltaday
            results.append(statistic)
        return results




    def anal_DeviceStatistic(self,queryHistory,device_id):
        '''
        for each device in the time range
        if fan or light:  {date: value,.....} 
        if temperature: {date: {max,min,meantemp,humid}...} 
        '''
        res = {}
        listDay_embedDatasInDay = {} # dictionary contain list =  {date: [{value,time}...]}
        date_list = [self.lt.date() - timedelta(days=x) for x in range(self.deltaday)]
        for i in date_list:
            listDay_embedDatasInDay.update({i:[]})
        for record in list(queryHistory):
            if record['device_id'] == device_id:
                if record['time'].date() in date_list:
                    listDay_embedDatasInDay[record['time'].date()].append({'value':record['value'],'time':record['time']})
        if self.type_dev == 'light' or self.type_dev == 'fan':
            prevDay = False
            for filteredRecord in listDay_embedDatasInDay:
                anal_inserted = self.anal_DayRecord_Fan_Light(listDay_embedDatasInDay[filteredRecord],prevDay,filteredRecord)
                res.update(anal_inserted[0])
                prevDay = anal_inserted[1]
            self.LastDayRecord = res[date_list[0]]
        elif self.type_dev == 'temperature':
            for filteredRecord in listDay_embedDatasInDay:
                anal_inserted = self.anal_DayRecordForTemp(listDay_embedDatasInDay[filteredRecord],filteredRecord)
                if anal_inserted!= None: res.update(anal_inserted)
        return res

    def anal_DayRecordForTemp(self,listData,filterDay):
        '''
        listData format : [{'value','time':dateobject},.....]
        '''
        minTemp = 100
        maxTemp = 0
        humid = 0
        count = 0
        if listData != []:
            for eachStatus in listData:
                gongcha = anal_value(eachStatus['value'],'temperature')
                cur_temp = int(gongcha[0])
                if(cur_temp > maxTemp): 
                    maxTemp = cur_temp - 0
                if(cur_temp < minTemp): 
                    minTemp = cur_temp - 0
                humid += int(gongcha[1])
                count+=1
            meanTemp = (minTemp + maxTemp)/2
            meanHumid = humid/count
            return {filterDay.strftime("%d/%m/%Y"):{'max-tempe': maxTemp,'min-tempe':minTemp,'mean-tempe':meanTemp,'humid':meanHumid}}
        else: return None


    def anal_DayRecord_Fan_Light(self,listData,previousDay,filterDay):
        '''
        listData format : [{'value','time':dateobject},.....]
        return [{day : totalTime}, ngay truoc co on k]
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
        if(filterDay < datetime.now().date() and isOn):
            deltatime = end_day - previous_time
            totalTime_1day += deltatime
        elif (isOn):
            ala = datetime.now() - previous_time  
            totalTime_1day += ala
        
        return tuple([{filterDay:(int(totalTime_1day.total_seconds()/36)/100)},isOn])  #filterday is date object (only date)



