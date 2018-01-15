#coding=utf-8
import requests
import json

data={"timestamp":1598965852,"longitude":108.6,"latitude":34.2}
r = requests.post('http://192.168.200.136:5005/dataserver', data)
print(r.text)
