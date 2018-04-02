# -*- coding: utf-8 -*-
from flask import Flask
from flask import request,jsonify
from influxdb import InfluxDBClient
from Lux import LuxS
from analyticaldata import analytical
from Noise import noisy
from ErrorHandle import CustomFlaskErr
import time,random
client = InfluxDBClient("192.168.200.136", 8086, "admin", "", "dataserverdb")

#db.create_database('testdb')
app = Flask(__name__)


def InquireDatasets(timestamp,measurement):
    measurement_hourly = measurement + "-hourly"
    measurement_day = measurement + "-day"
    fainaltime_last, fainaltime_now, fainaltime_today, fainaltime_yesterday = analytical.Analytical_time(timestamp)

    order_last = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_hourly, fainaltime_last)
    order_now = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_hourly, fainaltime_now)
    order_today = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_day, fainaltime_today)
    order_yesterday = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_day, fainaltime_yesterday)
    try:
        resposedata_last = client.query(order_last)
        resposedata_last = "{0}".format(resposedata_last)
        resposedata_now = client.query(order_now)
        resposedata_now = "{0}".format(resposedata_now)
        resposedata_today = client.query(order_today)
        resposedata_today = "{0}".format(resposedata_today)
        resposedata_yesterday = client.query(order_yesterday)
        resposedata_yesterday = "{0}".format(resposedata_yesterday)
    except Exception as e:
        print(e)
    finally:
        return resposedata_last,resposedata_now,resposedata_today,resposedata_yesterday


@app.route('/dataserver',methods=['POST'])
def info():
    try:
        timestamp = request.form.get("timestamp")
        timestamp = int(timestamp)


    except:
        raise CustomFlaskErr(500, status_code=400)
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
    measurement =analytical.select_area(latitude, longitude)
    measurement_hourly = measurement + "-hourly"
    measurement_day = measurement + "-day"
    try:
        resposedata_last, resposedata_now, resposedata_today, resposedata_yesterday = InquireDatasets(timestamp, measurement)
        fainaltime_last, fainaltime_now, fainaltime_today, fainaltime_yesterday = analytical.Analytical_time(timestamp)
        if resposedata_last == "ResultSet({})":
            timeArray = time.strptime(fainaltime_last, "%Y-%m-%d %H:%M:%S")
            lasttimestamp = time.mktime(timeArray)

            timeArray = time.localtime(lasttimestamp)
            fainaltime = time.strftime("%m-%d %H:%M:%S", timeArray)
            fainaltime = "2015-" + fainaltime

            order_last = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_hourly, fainaltime)
            resposedata_last = client.query(order_last)
            resposedata_last = "{0}".format(resposedata_last)
            resposedata_last = eval(analytical.Analytical_data(resposedata_last))

            resposedata_last["Temp(°C)"] = round((resposedata_last["Temp(°C)"] + random.uniform(-0.5, 0.5)), 1)
            resposedata_last["Humidity(%)"] = min((resposedata_last["Humidity(%)"] + random.randint(0, 5)),100)
            resposedata_last["WindSpeed(km/h)"] = round(max(resposedata_last["WindSpeed(km/h)"] + round(random.uniform(-0.5, 0.5), 1), 0.0),1)
            json_body = [
                {
                    "measurement": measurement_hourly,
                    "time": fainaltime_last,
                    "fields": {
                        "Temp(°C)": resposedata_last["Temp(°C)"],
                        "Humidity(%)":resposedata_last["Humidity(%)"],
                        "WindSpeed(km/h)": resposedata_last["WindSpeed(km/h)"]
                    }
                }
            ]
            #print("resposedata_last:",json_body)
            client.write_points(json_body)
        else:
            resposedata_last = "{0}".format(resposedata_last)
            resposedata_last = eval(analytical.Analytical_data(resposedata_last))

        if resposedata_now == "ResultSet({})":
            timeArray = time.strptime(fainaltime_now, "%Y-%m-%d %H:%M:%S")
            lasttimestamp = time.mktime(timeArray)

            timeArray = time.localtime(lasttimestamp)
            fainaltime = time.strftime("%m-%d %H:%M:%S", timeArray)
            fainaltime = "2015-" + fainaltime

            order_now = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_hourly, fainaltime)

            resposedata_now = client.query(order_now)
            resposedata_now = "{0}".format(resposedata_now)
            resposedata_now = eval(analytical.Analytical_data(resposedata_now))

            resposedata_now["Temp(°C)"] = round((resposedata_last["Temp(°C)"] + random.uniform(-0.5, 0.5)), 1)
            resposedata_now["Humidity(%)"] = min((resposedata_last["Humidity(%)"] + random.randint(0, 5)), 100)
            resposedata_now["WindSpeed(km/h)"] = round(max(resposedata_last["WindSpeed(km/h)"] + round(random.uniform(-0.5, 0.5), 1), 0.0), 1)

            json_body = [
                {
                    "measurement": measurement_hourly,
                    "time": fainaltime_now,
                    "fields": {
                        "Temp(°C)": resposedata_now["Temp(°C)"],
                        "Humidity(%)": resposedata_now["Humidity(%)"],
                        "WindSpeed(km/h)": resposedata_now["WindSpeed(km/h)"]
                    }
                }
            ]
            #print("resposedata_now:",json_body)
            client.write_points(json_body)
        else:
            resposedata_now = "{0}".format(resposedata_now)
            resposedata_now = eval(analytical.Analytical_data(resposedata_now))

        if  resposedata_today =="ResultSet({})":
            timeArray = time.strptime(fainaltime_today, "%Y-%m-%d %H:%M:%S")
            lasttimestamp = time.mktime(timeArray)

            timeArray = time.localtime(lasttimestamp)
            fainaltime = time.strftime("%m-%d %H:%M:%S", timeArray)
            fainaltime = "2015-" + fainaltime

            order_today = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_day, fainaltime)
            resposedata_today = client.query(order_today)
            resposedata_today = "{0}".format(resposedata_today)
            resposedata_today = eval(analytical.Analytical_data(resposedata_today))

            resposedata_today["rainfall(mm)"] = max(resposedata_today["rainfall(mm)"] + round(random.uniform(-0.5, 0.5), 1),0.0)
            resposedata_today["PM10(ug/m3)"] = max(int(resposedata_today["PM10(ug/m3)"] + random.randint(-30, 30)),30)
            resposedata_today["PM2.5(ug/m3)"] =max(int(resposedata_today["PM2.5(ug/m3)"] + random.randint(-30, 30)),30)
            resposedata_today["CO(mg/m3)"] =round( max(float(resposedata_today["CO(mg/m3)"] + random.uniform(-5.0, 5.0)),3.0), 1)
            resposedata_today["NO2(ug/m3)"] = max(int(resposedata_today["NO2(ug/m3)"] + random.randint(-10, 10)),8)
            resposedata_today["O3(ug/m3)"] = max(int(resposedata_today["O3(ug/m3)"] + random.randint(-10, 10)),8)
            resposedata_today["SO2(ug/m3)"] = max(int(resposedata_today["SO2(ug/m3)"] + random.randint(-5, 5)),3)

            json_body = [
                {
                    "measurement": measurement_day,
                    "time": fainaltime_today,
                    "fields": {
                        "PM10(ug/m3)": resposedata_today["PM10(ug/m3)"],
                        "PM2.5(ug/m3)": resposedata_today["PM2.5(ug/m3)"],
                        "CO(mg/m3)": resposedata_today["CO(mg/m3)"],
                        "NO2(ug/m3)": resposedata_today["NO2(ug/m3)"],
                        "O3(ug/m3)": resposedata_today["O3(ug/m3)"],
                        "rainfall(mm)": resposedata_today["rainfall(mm)"],
                        "SO2(ug/m3)": resposedata_today["SO2(ug/m3)"],
                    }
                }
            ]
            #print("fainaltime_today:",json_body)
            client.write_points(json_body)
        else:
            resposedata_today = "{0}".format(resposedata_today)
            resposedata_today = eval(analytical.Analytical_data(resposedata_today))

        if resposedata_yesterday == "ResultSet({})":

            timeArray = time.strptime(fainaltime_yesterday, "%Y-%m-%d %H:%M:%S")
            lasttimestamp = time.mktime(timeArray)

            timeArray = time.localtime(lasttimestamp)
            fainaltime = time.strftime("%m-%d %H:%M:%S", timeArray)
            fainaltime = "2015-" + fainaltime

            order_today = "select * from \"{0}\" WHERE time = '{1}'".format(measurement_day, fainaltime)
            resposedata_yesterday = client.query(order_today)
            resposedata_yesterday = "{0}".format(resposedata_yesterday)
            resposedata_yesterday = eval(analytical.Analytical_data(resposedata_yesterday))

            resposedata_yesterday["rainfall(mm)"] = max(resposedata_yesterday["rainfall(mm)"] + round(random.uniform(-0.5, 0.5), 1),
                                                0.0)
            resposedata_yesterday["PM10(ug/m3)"] = max(int(resposedata_yesterday["PM10(ug/m3)"] + random.randint(-30, 30)), 30)
            resposedata_yesterday["PM2.5(ug/m3)"] = max(int(resposedata_yesterday["PM2.5(ug/m3)"] + random.randint(-30, 30)),
                                                    30)
            resposedata_yesterday["CO(mg/m3)"] = round(max(float(resposedata_yesterday["CO(mg/m3)"] + random.uniform(-5.0, 5.0)), 3.0), 1)
            resposedata_yesterday["NO2(ug/m3)"] = max(int(resposedata_yesterday["NO2(ug/m3)"] + random.randint(-10, 10)), 8)
            resposedata_yesterday["O3(ug/m3)"] = max(int(resposedata_yesterday["O3(ug/m3)"] + random.randint(-10, 10)), 8)
            resposedata_yesterday["SO2(ug/m3)"] = max(int(resposedata_yesterday["SO2(ug/m3)"] + random.randint(-5, 5)), 3)

            json_body = [
                {
                    "measurement": measurement_day,
                    "time": fainaltime_yesterday,
                    "fields": {
                        "PM10(ug/m3)": resposedata_yesterday["PM10(ug/m3)"],
                        "PM2.5(ug/m3)": resposedata_yesterday["PM2.5(ug/m3)"],
                        "CO(mg/m3)": resposedata_yesterday["CO(mg/m3)"],
                        "NO2(ug/m3)": resposedata_yesterday["NO2(ug/m3)"],
                        "O3(ug/m3)": resposedata_yesterday["O3(ug/m3)"],
                        "rainfall(mm)": resposedata_yesterday["rainfall(mm)"],
                        "SO2(ug/m3)": resposedata_yesterday["SO2(ug/m3)"],
                    }
                }
            ]
            #print("fainaltime_today:", json_body)
            client.write_points(json_body)
        else:
            resposedata_yesterday = "{0}".format(resposedata_yesterday)
            resposedata_yesterday = eval(analytical.Analytical_data(resposedata_yesterday))


        luxss = LuxS(timestamp, latitude, longitude, 8, coe).GetLux()
        noise = noisy.noise(timestamp)

        resposedata = {}
        resposedata["time"] = timestamp
        resposedata["luxss"] = luxss
        resposedata["noise"] = noise
        resposedata["rl"] = resposedata_last
        resposedata["rn"] = resposedata_now
        resposedata["rt"] = resposedata_today
        resposedata["ry"] = resposedata_yesterday

        resposedata = analytical.update_noise_lux_data(resposedata)

    except:
        raise CustomFlaskErr(400, status_code=400)

    return resposedata.replace("\'","\"").replace("°C","C")


@app.errorhandler(CustomFlaskErr)
def handle_flask_error(error):

    # response 的 json 内容为自定义错误代码和错误信息
    response = jsonify(error.to_dict())

    # response 返回 error 发生时定义的标准错误代码
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def error_404(error):
    response = "erorr!!! not found route!!!"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,debug=True, threaded=True)
