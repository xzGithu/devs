import sqlite3
cx = sqlite3.connect("D:/py-source/devs/db.sqlite3")
cu=cx.cursor()
datas=[('127.0.0.1','/','disk_usage','%',15,123456754),('127.0.0.1','/','disk_usage','%',15,123456754),('127.0.0.1','/','disk_usage','%',15,123456754),('127.0.0.1','/','disk_usage','%',15,123456754),
('127.0.0.1','/','disk_usage','%',15,123456754),('127.0.0.1','/','disk_usage','%',15,123456754),('127.0.0.1','/','disk_usage','%',15,123456754),
]
sql='insert into devsapp_history_uint(endpoint, mpoint, itemid, uint,value,clock) values(?,?,?,?,?,?)'
cu.executemany(sql ,datas)
cx.commit()
cu.close()
cx.close()