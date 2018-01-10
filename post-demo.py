#coding=utf-8
import requests
import json

s = requests
data={"timestamp":5288970101,"longitude":104.3,"latitude":39.6}
#data = json.dumps(data)
#print("",type(data))
r = s.post('http://192.168.200.136:5002/dataserver', data)
print(r.text)
