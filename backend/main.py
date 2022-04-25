from cassandra.cluster import Cluster
import time

clstr=Cluster()
session=clstr.connect('httt')

qry = '''
drop table if exists button;
'''
session.execute(qry)
qry = '''
drop table if exists distance_sensor;
'''
session.execute(qry)
qry = '''
drop table if exists temperature_sensor;
'''
session.execute(qry)
qry = '''
drop table if exists information;
'''
session.execute(qry)
qry = '''
drop table if exists magenic_switch;
'''
session.execute(qry)



qry= '''
create table button (
    id int,
    data int,
    primary key(id)
);
'''
session.execute(qry)
qry = '''
create table distance_sensor (
    id int,
    distance int,
    duration int,
    valid int,
    primary key(id)
);
'''
session.execute(qry)
qry = '''
create table temperature_sensor (
    id int,
    temperature_object int,
    temperature_env int,
    primary key(id)
);
'''
session.execute(qry)
qry = '''
create table information (
    id int,
    valid_check int,
    primary key(id)
);
'''
session.execute(qry)
qry = '''
create table magenic_switch (
    id int,
    data int,
    primary key(id)
);
'''
session.execute(qry)


distance =  3
duration = 15
i=0
while True:
    i = i+1
    print("Sinh viên bấm nút đo nhiệt độ:...")
    print("bấm 1 để đo, 0 nếu không muốn đo")
    data = int(input()) #get from api adafruit 
    #button
    qry = """
    INSERT INTO button (id , data) 
    VALUES
    """ + str((i, 1))
    session.execute(qry)
    if data == 0:
        continue
    else:
        print("Mời bạn thực hiện đo nhiệt độ")
        print("Khoảng cách đo tối đa là:",distance," cm trong:", duration, " s" )
    
    ## distance sensor
    print("nhập 1 nếu đo hợp lệ")

    t_end = time.time() + 15
    valid = 0 #get from api
    while time.time() < t_end:
        valid = int(input())
        break
    
    qry = """
    INSERT INTO distance_sensor (id , distance, duration, valid) 
    VALUES
    """ + str((i, distance, duration, valid))
    session.execute(qry)

    if valid == 0:
        print("đo thất bại, đo lại nhé..")
        continue
    
    print("nhập nhiệt độ đo được:")
    print("nhiệt độ người:")
    temp_object = int(input())
    print("nhiệt độ môi trường")
    temp_env = int(input())


    qry = """
    INSERT INTO temperature_sensor (id , temperature_object, temperature_env) 
    VALUES
    """ + str((i, temp_object, temp_env))
    session.execute(qry)
    
    valid_check = 1
    if temp_object > 38:
        valid_check = 0
        print("nhiệt độ đã hơi cao rồi... không được vào cổng")
    else:
        print("vào cổng thoải mái bạn ey")
        
    qry = """
    INSERT INTO information (id , valid_check) 
    VALUES
    """ + str((i, valid_check))
    session.execute(qry)

    print("nhập thông tin cửa, mở rồi thì 1 ngược lại nhập 0")
    data = int(input())

    qry = """
    INSERT INTO magenic_switch (id , data) 
    VALUES
    """ + str((i, data))
    session.execute(qry)

    if data != valid_check:
        print("cửa bị lỗi rồi, sửa thôi")
    else:
        print("cửa hoạt động tốt.. người tiếp theo")