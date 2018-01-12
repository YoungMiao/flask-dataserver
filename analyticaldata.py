# -*- coding: utf-8 -*-
from __future__ import print_function
import random
import time
import re
from influxdb import InfluxDBClient
from Lux import LuxS
from Noise import noisy
from ErrorHandle import CustomFlaskErr

client = InfluxDBClient("localhost", 8086, "admin", "", "dataserverdb2")
class analytical():
    def Analytical_time(timestamp):
        # (type(timestamp))
        timestamp = timestamp - (timestamp % 3600)
        timeArray = time.localtime(timestamp)
        fainaltime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return fainaltime

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
                measurement = "demo-1"
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
    def update_noise_lux_data(noise,luxss,resposedata,measurement):
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
            client.write_points(json_body)
        return str(resposedata)

    def update_all_data(timestamp, latitude, longitude, coe, measurement):

        org_timestamp = 1420041600
        realtime = analytical.Analytical_time(timestamp)
        #print(realtime)
        if (timestamp > org_timestamp):
            timestamp1 = timestamp - 1420041600
            (old_year, old_day) = divmod(timestamp1, 31536000)
            sql_timestamp = org_timestamp - int(round(old_year / 4)) * 86400 + old_day
        else:
            (old_year, old_day) = divmod(timestamp, 31536000)
            sql_timestamp = org_timestamp + old_day
        ainaltime = (sql_timestamp // 86400-1)*86400+57600
        number = 0
        list_tem = []

        for i in range(24):

            request_time = (timestamp//86400-1)*86400+57600
            all_time = ainaltime + i * 3600
            request_time = request_time + i * 3600
            ltime = time.localtime(all_time)
            value = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
            request_ltime = time.localtime(request_time)
            request_value = time.strftime("%Y-%m-%d %H:%M:%S", request_ltime)
            #print(value,request_value)
            resposedata = client.query("select * from \"demo-1\" WHERE time = '{0}'".format(value))
            resposedata = "{0}".format(resposedata)
            resposedata = analytical.Analytical_data(resposedata)

            resposedata = eval(resposedata)
            resposedata["time"] = request_value


            resposedata["Wind speed"] = float(round((resposedata["Wind speed"] + random.random()), 1))
            resposedata["humidity"] = int(resposedata["humidity"] + random.randint(0, 5))
            resposedata["temperature"] = float(round((resposedata["temperature"] + random.random()), 1))
            if resposedata["humidity"] > 100:
                resposedata["humidity"] = 100
            number = number + resposedata["humidity"]
            list_tem.append([resposedata["temperature"], resposedata["humidity"], resposedata["Wind speed"],resposedata["time"],request_time])
        resposedata["humidity"] = number // 24

        if resposedata["humidity"] > 50:
            resposedata["rainfall"] = float(
                round((resposedata["rainfall"] + random.uniform(0, 0.5)), 1) * random.randint(0, 1))

        else:
            resposedata["rainfall"] = 0.0

        if resposedata["rainfall"] >= 0.5:
            resposedata["Pm10"] = max(random.randint(30, 50), int(resposedata["Pm10"] - random.randint(50, 100)))
            resposedata["Pm2_5"] = max(random.randint(30, 50), int(resposedata["Pm2_5"] - random.randint(50, 100)))
            resposedata["co"] = round(max(random.uniform(5.0, 10.0), (resposedata["co"] - random.uniform(0, 5.0))), 1)
            resposedata["no2"] = max(random.randint(5, 10), int(resposedata["no2"] - random.randint(0, 10)))
            resposedata["o3"] = max(random.randint(5, 10), int(resposedata["o3"] - random.randint(0, 10)))
            resposedata["so2"] = max(random.randint(5, 10), int(resposedata["so2"] - random.randint(0, 5)))
        else:
            resposedata["Pm10"] = int(resposedata["Pm10"] + random.randint(0, 50))
            resposedata["Pm2_5"] = int(resposedata["Pm2_5"] + random.randint(0, 50))
            resposedata["co"] = round(float(resposedata["co"] + random.uniform(0, 5.0)), 1)
            resposedata["no2"] = int(resposedata["no2"] + random.randint(0, 10))
            resposedata["o3"] = int(resposedata["o3"] + random.randint(0, 10))
            resposedata["so2"] = int(resposedata["so2"] + random.randint(0, 5))

        for k in range(len(list_tem)):
            request_time = list_tem[k][4]
            #print(request_time)
            luxss = LuxS(request_time, latitude, longitude, 8, coe).GetLux()
            noise = noisy.noise(request_time)
            resposedata["temperature"] = list_tem[k][0]
            resposedata["humidity"] = list_tem[k][1]
            resposedata["Wind speed"] = list_tem[k][2]
            resposedata["time"] = list_tem[k][3]
            json_body = [
                {
                    "measurement": measurement,
                    "time": resposedata["time"],
                    "fields": {
                        "temperature": resposedata["temperature"],
                        "humidity": resposedata["humidity"],
                        "Wind speed": resposedata["Wind speed"],
                        "Pm10": resposedata["Pm10"],
                        "Pm2_5": resposedata["Pm2_5"],
                        "co": resposedata["co"],
                        "no2": resposedata["no2"],
                        "o3": resposedata["o3"],
                        "rainfall": resposedata["rainfall"],
                        "so2": resposedata["so2"],
                        "noise": noise,
                        "lux": luxss
                    }
                }
            ]
            print(realtime,json_body)
            client.write_points(json_body)
        #time.sleep(2)
        resposedata1 = client.query("select * from \"demo-1\" WHERE time = '{0}'".format(realtime))
        resposedata1 = "{0}".format(resposedata1)
        resposedata1 = analytical.Analytical_data(resposedata1)
        #print(realtime,resposedata1)

        '''
        ainaltime = analytical.Analytical_time(sql_timestamp)
        resposedata = client.query("select * from \"demo-1\" WHERE time = '{0}'".format(ainaltime))
        resposedata = "{0}".format(resposedata)
        resposedata = analytical.Analytical_data(resposedata)
        resposedata = eval(resposedata)
        resposedata["time"] = realtime
        resposedata["Wind speed"] = round((resposedata["Wind speed"]+random.random()),1)
        resposedata["humidity"] = resposedata["humidity"]+random.randint(0,5)
        if resposedata["humidity"]>100:
            resposedata["humidity"] =100
        resposedata["temperature"] = round((resposedata["temperature"]+random.random()),1)
        resposedata["Pm10"] = resposedata["Pm10"]+random.randint(0,50)
        resposedata["Pm2_5"] = resposedata["Pm2_5"] + random.randint(0, 50)
        resposedata["noise"] = noise
        resposedata["lux"] = luxss
        resposedata["co"] = resposedata["co"] + random.randint(0, 5)
        resposedata["no2"] = resposedata["no2"] + random.randint(0, 10)
        resposedata["o3"] = resposedata["o3"] + random.randint(0, 10)
        resposedata["rainfall"] = round((resposedata["rainfall"] + random.random()),1)
        resposedata["so2"] = resposedata["so2"] + random.randint(0, 5)
        json_body = [
            {
                "measurement": measurement,
                "time": realtime,
                "fields": {
                    "temperature": resposedata["temperature"],
                    "humidity": resposedata["humidity"],
                    "Wind speed": resposedata["Wind speed"],
                    "Pm10": resposedata["Pm10"],
                    "Pm2_5": resposedata["Pm2_5"],
                    "co": resposedata["co"],
                    "no2":resposedata["no2"],
                    "o3": resposedata["o3"],
                    "rainfall": resposedata["rainfall"],
                    "so2":  resposedata["so2"],
                    "noise":noise,
                    "lux":luxss
                }
            }
        ]
        #client.write_points(json_body)
        '''
        return str(resposedata1)