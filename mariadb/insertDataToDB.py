#!/usr/bin/env python
# coding=utf-8

import requests
import pymysql
import csv
data = []
longitude = []
latitude = []
lampID = []
lampStatus = []
db = pymysql.connect(host='192.168.200.129',port=3306,user='root',passwd='root',db='test',charset='utf8mb4')
cursor = db.cursor()
header = True
#创建数据库
DB_NAME = 'lampinfoDB'
cursor.execute('DROP DATABASE IF EXISTS %s' %DB_NAME)
cursor.execute('CREATE DATABASE IF NOT EXISTS %s' %DB_NAME)
cursor.execute('use %s' %DB_NAME)


def createTable():
    cursor.execute("drop table if exists lampinfo_westavenue")
    #创建数据表
    sql = 'CREATE TABLE `lampinfo_westavenue` ( \
         `serialNumber`  varchar(50) NOT NULL, \
         `city`  varchar(50) NOT NULL, \
         `region`  varchar(50) NOT NULL, \
         `street`  varchar(50) NOT NULL, \
         `longitude`  FLOAT NULL, \
         `latitude`  FLOAT NULL, \
         `status`  INT NULL, \
         `circle`  varchar(50) NULL, \
         `controlWay` INT NULL, \
         `switchBox`  varchar(50) NULL, \
         `lampType` varchar(50) NULL,  \
         `lampCount` INT NULL, \
         `height`  INT NULL, \
         `manufacturer`  varchar(50) NULL, \
         `buildDepartment`  varchar(50) NULL, \
         `buildTime`  DATE NULL)'
    cursor.execute(sql)


def writeXBDDdatatoDB():
    #createTable()
    with open('LampInfo_westAvenue.csv', "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for line in reader:
            lon = float(line['lon'])
            lat = float(line['lat'])
            lampID = str(line['lampID'])
            lampStatus = int(line['lampStatus'])
            print(lon,lat,lampID,lampStatus)
            query = 'INSERT INTO lampinfo_westavenue(serialNumber, city, region, street, longitude, latitude, status, circle, controlWay,\
            switchBox, lampType,lampCount,height,manufacturer,buildDepartment,buildTime) ' \
                    'values(%s,\'西安市\',\'长安区\',\'西部大道\',%s,%s,%s,\'第一回路\',1,\'一号配电箱\',\'LED\',6,12,\'第一制造厂\',\'西安长城数字\',\'2018-02-15\')'
            args = (lampID, lon, lat, lampStatus)
            cursor.execute(query, args)

def writeXifengRoadDatatoDB():
    with open('LampInfo_xifengroad.csv', "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for line in reader:
            lon = float(line['lon'])
            lat = float(line['lat'])
            lampID = str(line['lampID'])
            lampStatus = int(line['lampStatus'])
            print(lon,lat,lampID,lampStatus)
            query = 'INSERT INTO lampinfo_xifengroad(serialNumber, city, region, street, longitude, latitude, status, circle, controlWay, switchBox, lampType,lampCount,height,manufacturer,buildDepartment,buildTime) ' \
                    'values(%s,\'西安市\',\'长安区\',\'西沣路\',%s,%s,%s,\'第二回路\',2,\'二号配电箱\',\'节能灯\',4,16,\'第二制造厂\',\'西安长城数字\',\'2018-03-25\')'
            args = (lampID, lon, lat, lampStatus)
            cursor.execute(query, args)

def writeXiTaiRoadDatatoDB():
    with open('LampInfo_xitairoad.csv', "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for line in reader:
            lon = float(line['lon'])
            lat = float(line['lat'])
            lampID = str(line['lampID'])
            lampStatus = int(line['lampStatus'])
            print(lon, lat, lampID, lampStatus)
            query = 'INSERT INTO lampinfo_xitairoad(serialNumber, city, region, street, longitude, latitude, status, circle, controlWay, switchBox, lampType,lampCount,height,manufacturer,buildDepartment,buildTime) ' \
                    'values(%s,\'西安市\',\'长安区\',\'西太路\',%s,%s,%s,\'第三回路\',3,\'三号配电箱\',\'白炽灯\',8,20,\'第三制造厂\',\'西安长城数字\',\'2018-05-03\')'
            args = (lampID, lon, lat, lampStatus)
            cursor.execute(query, args)
            
def writeNorthSecondRingRoadDatatoDB():
    with open('LampInfo_northSecondRing.csv', "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for line in reader:
            lon = float(line['lon'])
            lat = float(line['lat'])
            lampID = str(line['lampID'])
            lampStatus = int(line['lampStatus'])
            print(lon, lat, lampID, lampStatus)
            query = 'INSERT INTO LampInfo_northSecondRing(serialNumber, city, region, street, longitude, latitude, status, circle, controlWay, switchBox, lampType,lampCount,height,manufacturer,buildDepartment,buildTime) ' \
                    'values(%s,\'西安市\',\'未央区\',\'北二环\',%s,%s,%s,\'第三回路\',3,\'三号配电箱\',\'白炽灯\',8,20,\'第三制造厂\',\'西安长城数字\',\'2018-05-03\')'
            args = (lampID, lon, lat, lampStatus)
            cursor.execute(query, args)
            
if __name__ == '__main__':
    createTable()
    cursor.execute('drop table if exists lampinfo_xifengroad')
    cursor.execute('CREATE TABLE lampinfo_xifengroad LIKE lampinfo_westavenue')
    cursor.execute('drop table if exists LampInfo_xitairoad')
    cursor.execute('CREATE TABLE LampInfo_xitairoad LIKE lampinfo_westavenue')
    cursor.execute('drop table if exists LampInfo_northSecondRing')
    cursor.execute('CREATE TABLE LampInfo_northSecondRing LIKE lampinfo_westavenue')
    writeXBDDdatatoDB()
    writeXifengRoadDatatoDB()
    writeXiTaiRoadDatatoDB()
    writeNorthSecondRingRoadDatatoDB()
    db.commit()
    cursor.close()
    db.close()

