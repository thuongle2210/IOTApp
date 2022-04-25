from multiprocessing.connection import Client
from Adafruit_IO import Client, Feed, RequestError
import time
from cassandra.cluster import Cluster
import app

AIO_FEED_ID = "BBC_TEMP"
AIO_USERNAME = "thuongle2210"
AIO_KEY = "aio_Seoe53k3fcQox9jNxIfOdrQCGzKE"

aio = Client(AIO_USERNAME, AIO_KEY)



clstr=Cluster()
session=clstr.connect('httt')
import datetime
qry = '''
drop table if exists temperature;
'''
session.execute(qry)
qry= '''
create table temperature (
    name text,
    time double,
    data int,
    primary key(name, time, data)
)WITH CLUSTERING ORDER BY (time DESC, data ASC);
'''
session.execute(qry)

qry = '''
drop table if exists maybom;
'''
session.execute(qry)

qry = '''
create table maybom(
    name text,
    time double,
    data int,
    duration double,
    primary key(name, time, data)
)WITH CLUSTERING ORDER BY (time DESC, data ASC);
'''
session.execute(qry)

qry = '''
drop table if exists setting;
'''
session.execute(qry)

qry = '''
create table setting(
    name text,
    time double,
    TempThreshold int,
    HumdThreshold int,  
    primary key(name, time, TempThreshold)
)WITH CLUSTERING ORDER BY (time DESC, TempThreshold ASC);
'''
session.execute(qry)

isMaybom = 0
maybomStart = 0
Queue = [None]
tempThr = 30
while True:
    data = aio.receive('bbc-temp')
    if data in Queue:
        continue
    else:
        Queue.remove(Queue[-1])
        Queue.insert(0, data)
    time_create = time.time()
    temp = int(data.value)
    insert_data = str(('temp',time_create, temp))
    qry = """
    insert into temperature (name, time, data) values """ + insert_data
    print("temp:", data)
    session.execute(qry)
    
    """
    threshold
    """
    qry = "SELECT * FROM temperature"
    ex1 = session.execute(qry)
    print(list(ex1)[0].time)

    if temp>tempThr and isMaybom == 0:
        isMaybom = 1
        maybomStart = time_create
        qry = """
            insert into maybom (name, time, data, duration) values """ + str(('maybom', time_create, isMaybom, 0))
        session.execute(qry)
        print("maybom:",(time_create, isMaybom, 0))
    elif temp<=tempThr and isMaybom == 1:
        isMaybom = 0
        duration = time_create - maybomStart
        qry = """
            insert into maybom (name, time, data, duration) values """ + str(('maybom', time_create, isMaybom, duration))
        session.execute(qry)
        print("maybom:",(time_create, isMaybom, duration))
    time.sleep(8)
