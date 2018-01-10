# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from influxdb import InfluxDBClient
from Lux import LuxS
from analyticaldata import analytical
from Noise import noisy
import random

client = InfluxDBClient("localhost", 8086, "admin", "", "dataserverdb2")

#db.create_database('testdb')
app = Flask(__name__)

@app.route('/dataserver',methods=['POST'])
def info():
    timestamp = request.form.get("timestamp")
    timestamp = int(timestamp)
    fainaltime = analytical.Analytical_time(timestamp)
    noise = noisy.noise(timestamp)
    try:
        # 纬度
        latitude= request.form.get("latitude")

        # 经度
        longitude= request.form.get("longitude")
        assert latitude != None
        latitude = float(latitude)
        assert longitude != None
        longitude = float(longitude)
    except:
        latitude =  34.27
        longitude = 108.93
    try:
        coe = request.form.get("coe")
        assert coe != None
    except:
        coe = 0
    luxss = LuxS(timestamp, latitude, longitude, 8, coe).GetLux()
    measurement =select_area(latitude, longitude)

    print("11111",measurement)
    order ="select * from \"{0}\" WHERE time = '{1}'".format(measurement,fainaltime)
    try:
        resposedata = client.query(order)
        resposedata="{0}".format(resposedata)

        if resposedata == "ResultSet({})":
            resposedata = add_all_data(timestamp,noise,luxss,measurement)

        else:
            resposedata = analytical.Analytical_data(resposedata)
            resposedata = analytical.add_noise_lux_data(noise,luxss,resposedata,measurement)

    except Exception as e:
        resposedata="error!!! Parameter error!!!"

    return resposedata.replace("\'","\"")


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
            measurement="demo-1"
    else:
        measurement = "error!!! latitude and longitude are not in Xi'an!!!"
    return measurement

def add_all_data(timestamp,noise,luxss,measurement):
    #print(timestamp)
    org_timestamp = 1420041600
    realtime = analytical.Analytical_time(timestamp)
    if (timestamp>org_timestamp):
        timestamp1 = timestamp - 1420041600
        (old_year,old_day) = divmod(timestamp1, 31536000)
        sql_timestamp = org_timestamp - int(old_year/4)*86400+old_day
    else:
        (old_year, old_day) = divmod(timestamp, 31536000)
        sql_timestamp = org_timestamp + old_day
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
    return str(resposedata)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
