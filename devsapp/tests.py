import requests
import json
import random

datas = []
for i in range(1000):
    datas.append({
      "endpoint":"127.0.0.1",
      "mpoint":"",
      "itemid":"mem_usage",
      "uint":"%",
      "value": 50+random.randint(1, 20),
      "clock":1616830137+i,
      "dtypes":"int"
    })
data ={"data":datas}
print(data)

resp = requests.post('http://127.0.0.1:8000/get_data/',json.dumps(data))

