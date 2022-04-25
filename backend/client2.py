from multiprocessing.connection import Client
from Adafruit_IO import Client, Feed, RequestError
import time
from datetime import datetime

AIO_FEED_ID = "BBC_TEMP"
AIO_USERNAME = "thuongle2210"
AIO_KEY = "aio_Seoe53k3fcQox9jNxIfOdrQCGzKE"

aio = Client(AIO_USERNAME, AIO_KEY)


from cassandra.cluster import Cluster

clstr=Cluster()
session=clstr.connect('httt')
import datetime
qry = '''
drop table if exists temp;
'''
session.execute(qry)
qry= '''
create table temp (
id text,
data int,
insertion_time float,
primary key(id, insertion_time)
)WITH CLUSTERING ORDER BY (insertion_time DESC);
'''
session.execute(qry)


    
Queue = [None]
while True:
    data = aio.receive('bbc-temp')
    if data in Queue:
        continue
    else:
        Queue.remove(Queue[-1])
        Queue.insert(0, data)
    print(data)
    insert_data = str((time.time(),data.created_at, int(data.value)))
    qry = """
    insert into temp (insertion_time, id, data) values """ + insert_data
    #print(qry)
    session.execute(qry)
    time.sleep(3)

print(data.created_at)
print(type(data.created_at))