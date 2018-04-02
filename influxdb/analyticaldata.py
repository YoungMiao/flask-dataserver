# -*- coding: utf-8 -*-
from __future__ import print_function
import random
import time
import re
from influxdb import InfluxDBClient
from Lux import LuxS
from Noise import noisy
from ErrorHandle import CustomFlaskErr
import math

client = InfluxDBClient("localhost", 8086, "admin", "", "dataserverdb2")
class analytical():
    def Analytical_time(timestamp):
        # (type(timestamp))
        #timestamp = timestamp - (timestamp % 3600)
        timestamp_last = (timestamp//3600)*3600
        timestamp_now = int(math.ceil(timestamp/3600.0)*3600)
        timestamp_today = (timestamp//86400+1)*86400 + 14400
        timestamp_yesterday = (timestamp//86400)*86400 + 14400

        timeArray_last = time.localtime(timestamp_last)
        timeArray_now = time.localtime(timestamp_now)
        timeArray_today = time.localtime(timestamp_today)
        timeArray_yesterday = time.localtime(timestamp_yesterday)

        fainaltime_last = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_last)
        fainaltime_now = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_now)
        fainaltime_today = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_today)
        fainaltime_yesterday = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_yesterday)
        return fainaltime_last,fainaltime_now,fainaltime_today,fainaltime_yesterday

    def select_area(latitude, longitude):
        if longitude > 107.40 and longitude < 109.47 and latitude > 33.42 and latitude < 34.45:
            if longitude > 108.63 and longitude < 109.24 and latitude > 33.78 and latitude < 34.3:
                measurement = "changan"
            elif longitude > 108.90 and longitude < 108.99 and latitude > 34.23 and latitude < 34.27:
                measurement = "beilin"
            elif longitude > 109.09 and longitude < 109.46 and latitude > 34.28 and latitude < 34.74:
                measurement = "lintong"
            elif longitude > 108.94 and longitude < 109.03 and latitude > 34.24 and latitude < 34.30:
                measurement = "xincheng"
            elif longitude > 108.78 and longitude < 109.04 and latitude > 34.25 and latitude < 34.44:
                measurement = "weiyang"
            elif longitude > 109.15 and longitude < 109.43 and latitude > 34.59 and latitude < 34.75:
                measurement = "yanliang"
            elif longitude > 108.84 and longitude < 108.94 and latitude > 34.25 and latitude < 34.30:
                measurement = "lianhu"
            elif longitude > 108.98 and longitude < 109.27 and latitude > 34.16 and latitude < 34.45:
                measurement = "baqiao"
            elif longitude > 108.81 and longitude < 109.06 and latitude > 34.18 and latitude < 34.25:
                measurement = "yanta"
        else:
            raise CustomFlaskErr(404, status_code=400)
        return measurement

    def Analytical_data(str):
        pattern = r"(\[.*?\])";
        guid = re.findall(pattern, str, re.M)
        if (len(guid) > 0):
            guid = guid[0]
            guid = guid.replace('[', '').replace(']', '')
        return guid

    def update_noise_lux_data(resposedata_dict):
        resposedata = {}
        timestamp = resposedata_dict["time"]
        currentstamp = time.localtime(timestamp)
        current = time.strftime("%Y-%m-%d %H:%M:%S", currentstamp)
        resposedata["time"] = current

        resposedata_last =  resposedata_dict["rl"]
        resposedata_now = resposedata_dict["rn"]
        resposedata_today = resposedata_dict["rt"]
        resposedata_yesterday = resposedata_dict["ry"]
        for k,v in resposedata_last.items():
            if k != "time":
                resposedata[k] = round(float(v)+ ((float(resposedata_now[k]) - float(v))/3600)*(timestamp%3600),1)
        for k, v in resposedata_yesterday.items():
            if k != "time":
                resposedata[k] = round(float(v) + ((float(resposedata_today[k]) - float(v))/ 86400) * (timestamp % 86400), 1)
        if not "noise" in resposedata.keys():
            resposedata["lux"] = resposedata_dict["luxss"]
            resposedata["noise"] = resposedata_dict["noise"]


        return str(resposedata)
