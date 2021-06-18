from API.models import *
from bson.json_util import ObjectId
import json
from ast import literal_eval

PYTHON_DAY_TO_DB_DAY_MAP = {
    6: 1, 
    0: 2, 
    1: 3, 
    2: 4, 
    3: 5, 
    4: 6, 
    5: 7, 
}
from datetime import time, datetime
from pytz import timezone, utc

def getTime(stringTime: str):
    hour, minute = [int(x) for x in stringTime.split(":")]
    return time(hour, minute)

def job(adaAccesses: dict, feedNameToUser: dict):
    try:
        datenow = datetime.utcnow().replace(second=0, microsecond=0)
        datenow = utc.localize(datenow, is_dst=None).astimezone(timezone("Asia/Saigon"))
        timenow = datenow.time()
        # print("------------")
        # print("time now: " + str(timenow) + " | " + str(datenow.weekday()))
        schedules = Schedule.objects.all()
        # print("No of SChedules: " + str(len(schedules)))
        for schedule in schedules:
            time_on = getTime(schedule.time_on)
            time_off = getTime(schedule.time_off)
            # print("time_on: " + str(time_on))
            # print(time_on == timenow)
            # print("time_off: " + str(time_off))
            # print(time_off == timenow)
            # print("Automode")
            device = None
            try:
                device = Device.objects.get(_id=ObjectId(schedule.device_id))
            except Exception as e:
                print("Can't find the device with id " + schedule.device_id)
                print(e)
            if not device:
                continue
            # print(device.automation_mode == 1)
            # print("-")

            if device.automation_mode != 1:
                continue
            
            if device.feed_name in feedNameToUser:
                deviceAccess = adaAccesses[feedNameToUser[device.feed_name]]
            else:
                print("Can't map feed name to user. Feed name: " + device.feed_name)
                continue
            
            data_form = {"id":"","name":"","data":"","unit":""}
            if(device.unit == None):
                data_form["unit"] = ""
            else:  data_form["unit"] = device.unit
            data_form["id"] = device.data_id
            data_form["name"] = device.control_type

            if not schedule.is_repeat:
                if time_on == timenow:
                    if device.status == "1":
                        continue
                    data_form["data"] = "1"
                    # print("Sending data to adafruit")
                    deviceAccess.sendDataToFeed(device.feed_name, str(json.dumps(data_form)))
                    continue

                elif time_off == timenow:
                    if device.status == "0":
                        schedule.delete()
                        continue
                    data_form["data"] = "0"
                    deviceAccess.sendDataToFeed(device.feed_name, str(json.dumps(data_form)))
                    schedule.delete()
                    continue

            else:
                repeat_days = literal_eval(schedule.repeat_day)
                if time_on == timenow:
                    if device.status == "1":
                        continue
                    if PYTHON_DAY_TO_DB_DAY_MAP[datenow.weekday()] in repeat_days:
                        data_form["data"] = "1"
                        deviceAccess.sendDataToFeed(device.feed_name, str(json.dumps(data_form)))
                        continue

                elif time_off == timenow:
                    if device.status == "0":
                        continue
                    if PYTHON_DAY_TO_DB_DAY_MAP[datenow.weekday()] in repeat_days:
                        data_form["data"] = "0"
                        deviceAccess.sendDataToFeed(device.feed_name, str(json.dumps(data_form)))
    except Exception as e:
        print(e)