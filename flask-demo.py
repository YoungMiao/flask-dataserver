# -*- coding: utf-8 -*-
from flask import Flask
from flask import request,jsonify
from influxdb import InfluxDBClient
from Lux import LuxS
from analyticaldata import analytical
from Noise import noisy
from ErrorHandle import CustomFlaskErr
client = InfluxDBClient("localhost", 8086, "admin", "", "dataserverdb2")

#db.create_database('testdb')
app = Flask(__name__)

@app.route('/dataserver',methods=['POST'])
def info():
    try:
        timestamp = request.form.get("timestamp")
        timestamp = int(timestamp)
        fainaltime = analytical.Analytical_time(timestamp)
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

    order ="select * from \"{0}\" WHERE time = '{1}'".format(measurement,fainaltime)
    try:
        resposedata = client.query(order)
        resposedata="{0}".format(resposedata)

        if resposedata == "ResultSet({})":
            resposedata = analytical.update_all_data(timestamp,latitude, longitude,coe,measurement)

        else:
            resposedata = analytical.Analytical_data(resposedata)
            luxss = LuxS(timestamp, latitude, longitude, 8, coe).GetLux()
            noise = noisy.noise(timestamp)
            resposedata = analytical.update_noise_lux_data(noise,luxss,resposedata,measurement)

    except:
        raise CustomFlaskErr(400, status_code=400)

    return resposedata.replace("\'","\"")

# 用户名输入为空
    if user_name is None:
        raise CustomFlaskErr(USER_NAME_ILLEGAL, status_code=400)

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
    app.run(host='0.0.0.0', port=5005,debug=True)
