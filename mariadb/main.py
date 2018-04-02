# -*- coding:UTF-8 -*-
from flask import Flask, request, json
from werkzeug.utils import secure_filename
import os
import time
import pymysql
import csv

#from builtins import print

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])

database = "lampinfoDB"
db = pymysql.connect(host='192.168.200.129', port=3306, user='root', passwd='root',db='lampinfoDB',charset='utf8mb4')
#  获取操作游标
cursor = db.cursor()
# SQL 查询语句
cursor.execute("use lampinfoDB")
#db_label = "lampinfo_xifengroad"
cursor.execute("show tables")
g_tables = cursor.fetchall()
print(str(g_tables))

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/operate', methods=['POST'])
def operate():
    method = request.form.get("methodinfo")
    print("method:",method)
    db_label = request.form.get("db_label")
    if method =="add-table":
        upload_files = request.files.getlist("field1")
        for upload_file in upload_files:
            if upload_file and allowed_file(upload_file.filename):
                filename = secure_filename(upload_file.filename)
                upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
                # return 'hello, '+request.form.get('name', 'little apple')+'. success'
                time.sleep(1)
                db_label = filename.split(".")[0]
                response = add_table(db_label)
                with open(filename) as csvfile:
                    sp = csv.DictReader(csvfile)
                    for row in sp:
                        if row["serialNumber"] != "":
                            sql = "insert into {0} (serialNumber,city,region,street,longitude,latitude,height,manager) values('%s','%s','%s','%s','%s','%s','%s','%s')".format(db_label)
                            data = (row["serialNumber"], row["city"], row["region"], row["street"], row["longitude"], row["latitude"], row["height"], row["manager"])
                            cursor.execute(sql % data)
                print('数据库',db_label,'成功插入', cursor.rowcount, '条数据')
                db.commit()
                response = "add success!!!"
            else:
                response = "File format error, please select csv file"
    elif method == "delete-table":
        response =  delete_table(db_label)
    elif method == "get-table":
        response = get_tabel(db_label)
    elif method == "insert":
        insertdatalist = request.values.getlist("insertdata")
        for instertdata in insertdatalist:
            instertdata = json.loads(instertdata.replace("'","\""))
            response = insert_data(db_label,instertdata)
    elif method == "delete":
        serialNumber = request.form.get("serialNumber")
        response = delete_data(db_label,serialNumber)
    elif method == "update":
        serialNumber = request.form.get("serialNumber")
        updatedatalist = request.form.getlist("update")
        for updatedata in updatedatalist:
            print(updatedata)
            updatedatas = json.loads(updatedata.replace("'","\""))
            print(type(updatedatas), updatedatas)
            for key,value in updatedatas.items():
                response = update_data(serialNumber,db_label,key,value)
    elif method == "get-all-tables":
        response = get_all_tables();
    else:
        response = "error,the method is wrong!!!"
    return response

def formatResponseData(response):
    print("response", response)
    jsondata = []
    for row in response:
        print(row)
        result = {}
        result["lampId"] = str(row[0])
        result["city"] = str(row[1])
        result["region"] = str(row[2])
        result["street"] = str(row[3])
        result["longitude"] = row[4]
        result["latitude"] = row[5]
        result["status"] = row[6]
        result["circle"] = row[7]
        result["controlWay"] = str(row[8])
        result["switchBox"] = str(row[9])
        result["lampType"] = str(row[10])
        result["lampCount"] = str(row[11])
        result["height"] = row[12]
        result["manufacturer"] = row[13]
        result["buildDepartment"] = row[14]
        result["buildTime"] = str(row[15])
        jsondata.append(result)
    jsondatar = json.dumps(jsondata, ensure_ascii=False)
    print(jsondatar)
    return jsondatar;
    
def get_all_tables():
    response = ()
    try:
        cursor.execute("use lampinfoDB")
        for table in g_tables:
            print("table: ",str(table[0]));
            cursor.execute("select * from {0} ORDER BY serialNumber ASC".format(table[0]))
            db.commit()
            result = cursor.fetchall()
            response = response + result;
    except Exception as e:
        print("Error:unable to get data", e)
        response = str(e)
    finally:
       response = formatResponseData(response)
       return response

def get_tabel(db_label):
    #cursor.execute("use demo_1")
    results = ()
    try:
        # 执行SQL语句
        print(db_label)
        cursor.execute("use lampinfoDB")
        cursor.execute("select * from {0} ORDER BY serialNumber ASC ".format(db_label))
        db.commit()
        # 获取所有记录列表
        #results = "".join(cursor.fetchall())
        results = cursor.fetchall()
    except Exception as e:
        print("Error: unable to get data", e)
        return str(e)
    finally:
        response = formatResponseData(results)
        return response

def add_table(db_label):
    try:
        #cursor.execute("use demo_1")
        sql = """create table {0}(serialNumber VARCHAR(50) COLLATE utf8_bin NOT NULL,city VARCHAR(50 )COLLATE utf8_bin NOT NULL,region VARCHAR(50) COLLATE utf8_bin NOT NULL,street VARCHAR(50) COLLATE utf8_bin NOT NULL,longitude VARCHAR(50) COLLATE utf8_bin NOT NULL,latitude VARCHAR(50) COLLATE utf8_bin NOT NULL,height VARCHAR(50) COLLATE utf8_bin NOT NULL,manager VARCHAR(50) COLLATE utf8_bin NOT NULL)""".format(db_label)
        # 如果表存在则删除
        cursor.execute("drop table if exists {0}".format(db_label))
        # 创建表
        cursor.execute(sql)
        db.commit()
        response = "add {0} success!!!".format(db_label)
    except Exception as e:
        print("Error: unable to add data", e)
        response = str(e)
    finally:
        return response
def delete_table(db_label):
    try:
        #cursor.execute("use demo_1")
        # 如果表存在则删除
        cursor.execute("drop table if exists {0}".format(db_label))
        db.commit()
        response = "delete {0} success!!!".format(db_label)
    except Exception as e:
        print("Error: unable to delete data", e)
        response = str(e)
    finally:
        return response
def insert_data(db_label,insertdata):
    try:
        inquiry = """show tables like '{0}'""".format(db_label)
        if (cursor.execute(inquiry) == 1):
            sql = "insert into {0} (serialNumber,city,region,street,longitude,latitude,height,manager) values('%s','%s','%s','%s','%s','%s','%s','%s')".format(db_label)
            data = (insertdata["serialNumber"], insertdata["city"], insertdata["region"], insertdata["street"], insertdata["longitude"], insertdata["latitude"],insertdata["height"], insertdata["manager"])
            cursor.execute(sql % data)
            db.commit()
            response = "insert success!!!"
        else:
            response =  "table does not exist"
    except Exception as e:
        print("Error: database operation failed!!!",e)
        response = str(e)
    finally:
        return response
def delete_data(db_label,serialNumber):
    try:
        inquire = "select serialNumber from {0} where serialNumber={1}".format(db_label,serialNumber)
        print(inquire)
        if cursor.execute(inquire) == 1:
            sql =  "delete from {0} where serialNumber={1}".format(db_label,serialNumber)
            cursor.execute(sql)
            db.commit()
            response = "delete success!!!"
        else:
            response = "Error: serialNumber = {0} not found in the database".format(serialNumber)
    except Exception as e:
        print("Error: database operation failed!!!",e)
        response = str(e)
    finally:
        return response
def update_data(serialNumber,db_label,key,value):
    try:
        sql = " update {0} set {1}='{2}' where  serialNumber = '{3}'".format(db_label,key,value,serialNumber)
        cursor.execute(sql)
        db.commit()
        response = "update success!!!"
    except Exception as e:
        print("Error: database operation failed!!!", e)
        response = str(e)
    finally:
        return response

@app.route('/validate', methods=['POST'])
def validate():
    method = request.form.get("methodinfo")
    username = request.form.get("username")
    password = request.form.get("password")
    if method =="validate-user":
        response = validate_user(username, password)
    return response
#验证用户名和密码是否正确，返回值为如下格式
#{
#    "ret":"true",
#    "userid":id
# }
def validate_user(username, password):
    #执行SQL语句
    print("username:",username,"password:",password)
    response = {}
    response["status"] = False;
    response["userId"] = -1;
    cursor.execute("use lampinfoUserAccessDB")
    cursor.execute("select * from lampinfo_users")
    db.commit();
    #获取所有记录列表
    result = cursor.fetchall();
    for row in result:
        userID = str(row[0])
        user = str(row[1])
        passwd = str(row[2])
        print(userID, user, passwd)
        if(user == username and passwd == password):
            response["status"] = True
            response["userId"] = userID
    jsondatar = json.dumps(response, ensure_ascii=False)
    print(jsondatar)
    return jsondatar;

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005,debug=True)
    cursor.close()
    db.close()