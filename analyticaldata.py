# -*- coding: utf-8 -*-
from __future__ import print_function
import random
import time
import re
from influxdb import InfluxDBClient

client = InfluxDBClient("localhost", 8086, "admin", "", "dataserverdb2")
class analytical():
    def Analytical_time(timestamp):
        #print(type(timestamp))
        timestamp = timestamp - (timestamp % 3600)
        timeArray = time.localtime(timestamp)
        fainaltime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return fainaltime

    def Analytical_data(str):
        pattern = r"(\[.*?\])";
        guid = re.findall(pattern, str, re.M)
        if (len(guid) > 0):
            guid = guid[0]
            guid = guid.replace('[', '').replace(']', '')
        return guid
    def add_noise_lux_data(noise,luxss,resposedata,measurement):
        resposedata = eval(resposedata)
        if not "noise" in resposedata.keys():
            resposedata["lux"] = luxss
            resposedata["noise"] = noise
            json_body = [
                {
                    "measurement": measurement,
                    "time": resposedata["time"],
                    "fields": {
                        "lux": luxss,
                        "noise": noise
                    }
                }
            ]
            #client.write_points(json_body)
        return str(resposedata)