import requests
import json


data ={"data":[{
  "endpoint":"127.0.0.1",
  "mpoint":"/",
  "itemid":"disk_usage",
  "uint":"%",
  "value":15,
  "clock":123456754,
  "dtypes":"int"
},{
  "endpoint":"127.0.0.1",
  "mpoint":"/",
  "itemid":"disk_usage",
  "uint":"%",
  "value":15,
  "clock":123456754,
  "dtypeq":""
}]}
resp = requests.post('http://127.0.0.1:8000/get_data/',json.dumps(data))

