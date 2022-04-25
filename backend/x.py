import requests

url = 'http://127.0.0.1:5000/settingConfig'
myobj = {'tempThr': 30, 'humdThr':40}

x = requests.post(url, data = myobj, json= {'a':1})

print(x.text)