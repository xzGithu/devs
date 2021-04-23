import requests
import json
import random
import time

datas = []
for i in range(10):
    datas.append({
      "endpoint":"192.168.1.1",
      "mpoint":"",
      "itemid":"disk_usage",
      "uint":"%",
      "value": 50+random.randint(1, 20),
      "clock":int(time.time())+i,
      "dtypes":"int"
    })
data ={"data":datas}
print(data)

resp = requests.post('http://127.0.0.1:8000/get_data/',json.dumps(data))

