import json
import requests
import time
import json



def get_sensor_data_stream():
    try:
        url = 'http://127.0.0.1:5000/alldata'
        r = requests.get(url)
        return r.text
    except:
        return "Error in Connection"

while True:
    msg =  get_sensor_data_stream()
    print(type(msg))
    print(msg[1:-2])
    msg = msg[1:-2]
    #msgtodict = json.loads(msg)
    #print(type(msgtodict))
    #print(json.loads(msg))
    #print(msgtodict['system.avg(data)'])
    break
    time.sleep(4)
