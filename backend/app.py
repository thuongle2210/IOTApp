#example_app.py
import imp
from math import expm1
from re import L
import uuid
from flask import Flask, jsonify
from flask import Blueprint
from flask_cqlalchemy import CQLAlchemy
from flask import request
from cassandra.cluster import Cluster
import time
from Adafruit_IO import Client, Feed, RequestError, MQTTClient
import sys



app = Flask(__name__)

clstr=Cluster()
session=clstr.connect('httt')
'''
setting
'''
tempThr = 30
humdThr = 50



@app.route('/alldata', methods=['GET'])
def alldata():
    qry = "select * from temperature"
    ex1 = session.execute(qry)
    return jsonify(list(ex1))

@app.route('/max', methods=['GET'])
def max():
    qry = "SELECT max(data) FROM temperature;"
    ex1 = session.execute(qry)
    return jsonify(list(ex1))

@app.route('/min', methods=['GET'])
def min():
    qry = "SELECT min(data) FROM temperature;"
    ex1 = session.execute(qry)
    return jsonify(list(ex1))

@app.route('/average', methods=['GET'])
def avg():
    qry = "SELECT avg(data) FROM temperature;"
    ex1 = session.execute(qry)
    print(type(ex1))
    return jsonify(list(ex1))

@app.route('/newest', methods=['GET'])
def newest():
    qry = "SELECT * FROM temperature WHERE name='temp' ORDER BY time DESC  LIMIT 1;"
    ex1 = session.execute(qry)
    a = list(ex1)
    # print(ex1)
    # print("type", ex1)
    # print("hahahaha")
    return jsonify(a)

@app.route('/top', methods=['GET'])
def top ():
    args = request.args.get('number')

    qry = "SELECT * FROM temperature WHERE name='temp' ORDER BY time DESC  LIMIT " +args +";"
    ex1 = session.execute(qry)
    a = list(ex1)
    l = jsonify(a)
    print("l nek", l)
    return l
@app.route('/maybomStatus', methods=['GET'])
def maybomStatus():
    qry = "SELECT * FROM maybom WHERE name='maybom' ORDER BY time DESC  LIMIT 1"
    ex1 = session.execute(qry)
    a = list(ex1)
    l = jsonify(a)
    print("l nek", l)
    return l

@app.route('/settingDetails', methods=['GET'])
def settingDetails():
    qry = "SELECT * FROM setting WHERE name='setting' ORDER BY time DESC LIMIT 1"
    ex1 = session.execute(qry)
    a = list(ex1)
    l = jsonify(a)
    print("l nek", l)
    return l

@app.route('/settingConfig', methods=['POST'])
def settingConfig():
    global tempThr
    global humdThr  
    tempThr = request.form.get('tempThr')
    humdThr = request.form.get('humdThr')
    insert_values = ('setting', time.time(),int(tempThr), int(humdThr))    
    qry = """insert into setting(name, time, TempThreshold, HumdThreshold) values"""  + str(insert_values)
    ex1 = session.execute(qry)
    return "accept"
if __name__ == "__main__":
    app.run()


