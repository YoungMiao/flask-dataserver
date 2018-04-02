import requests
import json

#files = {
#    ("field1", ("gaoxinload.csv", open("./org/gaoxinload.csv", 'rb'),'multipart/form-data')),
#    ("field1", ("kejiload.csv", open("./org/kejiload.csv", 'rb'),'multipart/form-data'))
#}
#dictdata = {"serialNumber":"01010200010003","city":"西安","region":"高新区","street":"高新路","longitude":"106.548 ","latitude":"39.2458 ","height":"12 ","manager":"王五"}
#dictdata = [{"serialNumber":"01010200010003","city":"西安","region":"高新区","street":"高新路","longitude":"106.548 ","latitude":"39.2458 ","height":"12 ","manager":"王五"},{"serialNumber":"01010200010004","city":"西安","region":"高新区","street":"高新路","longitude":"106.548 ","latitude":"39.2458 ","height":"12 ","manager":"王五"}]

#dictdata = json.dumps(dictdata)
#dictdata = json.loads(dictdata)
#print(type(dictdata),dictdata)
#update = [{"manager":"王麻子"}]
#data = {"methodinfo":"update","db_label":"gaoxinload","insertdata":dictdata,"serialNumber":"01010200010001","update":update}
#str_data = json.dumps(data)
#json_data = json.loads(str_data)

#data = {"methodinfo":"get-all-tables", "db_label":""}
#data = {"methodinfo":"get-table", "db_label": "lampinfo_xifengroad"}
#r = requests.post("http://192.168.200.129:5005/operate",data=data)

data = {"methodinfo":"validate-user", "username":"admin", "password":"admin"}
r = requests.post("http://192.168.200.129:5005/validate",data=data)
print(r.text)
