# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:51:47 2018

@author: garima.misra


ALL
--START ADDRESS LIST AND EXISTS
--END ADDRESS LIST AND EXISTS
--FROM START TO END WITH DATE 
#Below two can be integrated in a single method also: all dates will be taken for a given combination 
--FROM START TO END WITHOUT DATE 
--TRAFFIC ON A PARTICULAR DATE 
current_app context

"""


import numpy as np
import time
import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, render_template, abort, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db
from models import DelhiTraffic, MumbaiTraffic, BangloreTraffic
from custom import ValidationError, NotFoundError, ServerError, Validation 
#from views import Validation


api = Flask(__name__)
api.config.from_pyfile('Config.py')


@api.route('/v1/Cities/')
def Cities():
    data = {'City_List' : ['Delhi', 'Mumbai', 'Banglore']}
    return jsonify(data)


@api.route('/v1/check_data_meta/')
def check_Data_Meta():
    x = DelhiTraffic.query.all()
    print(len(x))
    print(x)
    print(type(x[1]))
    print(type(x[1].distance))
    print(type(x[1].duration))
    print(type(x[1].duration_traffic))
    print(type(x[1].end_address))
    print(type(x[1].start_address))
    print(type(x[1].t))
    print(type(x[1].speed_no_traffic))
    print(type(x[1].speed_w_traffic))
    print(type(x[1].t_human))
    print(type(x[1].route))
    
    return(jsonify({'check_data' : DelhiTraffic.query.all()}))



@api.route('/v2/traffic/', methods = ['GET'])
def traffic2():
    #FROM START TO END WITH DATE
    try:
        if request.args.get('city'):
            city = request.args.get('city')
        else: 
            city = "Delhi"
        
        if request.args.get('date_time'):
            date_time = request.args.get('date_time')         #Check date length and format and existance in database    
        else:
            date_time = "201706130430"
        
        if request.args.get('start_station'):
            start_station = request.args.get('start_station')
        else:
            start_station = "MSIL Internal Rd, Maruti Udyog, Sector 18, Gurugram, Haryana 122008, India"
            
        if request.args.get('end_station'):
            end_station = request.args.get('end_station')
        else:
            end_station = "Civil Lines, Gurugram, Haryana 122022, India"
                      
    except ValueError as valueerr:
        print("ValueError has been raised." )
        print(valueerr)
    except TypeError as typeerr:
        print("Type error has been raised.")
        print(typeerr)
        
    if city == "Delhi":
        conn = DelhiTraffic
    elif city == "Banglore":
        conn = BangloreTraffic
    elif city == "Mumbai":
        conn = MumbaiTraffic
    else:
        conn = DelhiTraffic
    
    Validation.date_time_validation(conn, date_time)
    Validation.city_validation(conn, city)
    Validation.end_station_validation(conn, end_station)
    Validation.start_station_validation(conn, start_station)
        
    
    print(type(date_time))
    print(date_time)
    print(start_station)
    print(end_station)
    data_db = conn.query.filter(conn.start_address.like('%'+start_station+'%'), 
                                conn.end_address.like('%'+end_station+'%'), conn.t == date_time).all()
    print(len(data_db))
    print(data_db)
    if(len(data_db) == 0):
        raise NotFoundError({'start_station' : start_station, 'date_time' : date_time, 
                             'end_station' : end_station}, message = 'This combination doesn\'t match any record')
    else:
        start_time = time.time()
        data = { i+1 : {'Distance': data_db[i].distance, 'Duration' : data_db[i].duration, 
                        'Duration_Traffic' : data_db[i].duration_traffic, 'End_Address' : data_db[i].end_address, 
                        'Start_Address' : data_db[i].start_address, 'Speed_Without_Traffic' : data_db[i].speed_no_traffic, 
                        'Speed_With_Traffic' : data_db[i].speed_w_traffic, 'Time' : data_db[i].t_human,  
                        'Route' : data_db[i].route} 
                for i in range(len(data_db))}
        traffic_data = {'traffic_data' : data}
        print(traffic_data)
        del (data)
        end_time = time.time()
        print("time taken ", end_time - start_time)
        return jsonify(traffic_data)


 
@api.route('/v2/traffic/date/', methods = ['GET'])
def traffic_date():
    #TRAFFIC ON A PARTICULAR DATE 
    try:
        if request.args.get('date_time'):
            date_time = request.args.get('date_time')
        else:
            date_time = '201706130430'
        
        if request.args.get('city'):
            city = request.args.get('city')
        else:
            city = 'Delhi'
            
    except ValueError as valueerr:
        print("ValueError has been raised." )
        print(valueerr)
    except TypeError as typeerr:
        print("Type error has been raised.")
        print(typeerr)
        
    
    if city == "Delhi":
        conn = DelhiTraffic
    elif city == "Banglore":
        conn = BangloreTraffic
    elif city == "Mumbai":
        conn = MumbaiTraffic
    else:
        conn = DelhiTraffic
        
    Validation.date_time_validation(conn, date_time)
    Validation.city_validation(conn, city)
    
    data_db = conn.query.filter(conn.t.like('%'+date_time+'%'))
   
    start_time = time.time()
    data = {}
    for i in range((data_db).count()):
        print(i)
        data[i + 1] = {'Distance': data_db[i].distance, 'Duration' : data_db[i].duration, 
                        'Duration_Traffic' : data_db[i].duration_traffic, 
                        'End_Address' : data_db[i].end_address, 'Start_Address' : data_db[i].start_address, 
                        'Speed_Without_Traffic' : data_db[i].speed_no_traffic, 'Speed_With_Traffic' : data_db[i].speed_w_traffic,
                        'Time' : data_db[i].t_human,  'Route' : data_db[i].route}
        print(data_db[i])
    traffic_data = {'traffic_data' : data}
    del (data)
    end_time = time.time()
    print("time taken ", end_time - start_time)
    return jsonify(traffic_data)



@api.route('/v2/traffic/start/end/', methods = ['GET'])
def traffic_start_end():
    #FROM START TO END WITHOUT DATE
    try:
        if request.args.get('city'):
            city = request.args.get('city')
        else: 
            city = "Delhi"
        
        if request.args.get('start_station'):
            start_station = request.args.get('start_station')
        else:
            start_station = "MSIL Internal Rd, Maruti Udyog, Sector 18, Gurugram, Haryana 122008, India"
            
        if request.args.get('end_station'):
            end_station = request.args.get('end_station')
        else:
            end_station = "Civil Lines, Gurugram, Haryana 122022, India"
                      
    except ValueError as valueerr:
        print("ValueError has been raised." )
        print(valueerr)
    except TypeError as typeerr:
        print("Type error has been raised.")
        print(typeerr)
        
    if city == "Delhi":
        conn = DelhiTraffic
    elif city == "Banglore":
        conn = BangloreTraffic
    elif city == "Mumbai":
        conn = MumbaiTraffic
    else:
        conn = DelhiTraffic
        
    Validation.city_validation(conn, city)
    Validation.end_station_validation(conn, end_station)
    Validation.start_station_validation(conn, start_station)
        
    print(start_station)
    print(end_station)
    data_db = conn.query.filter(conn.start_address.like('%'+start_station+'%'), conn.end_address.like('%'+end_station+'%')).all()
    print(len(data_db))
    print(data_db)
    if(len(data_db) == 0):
        raise NotFoundError({'start_station' : start_station,'end_station' : end_station}, 
                            message = 'This combination doesn\'t match any record')
    else:
        start_time = time.time()
        data = { i+1 : {'Distance': data_db[i].distance, 'Duration' : data_db[i].duration,
                        'Duration_Traffic' : data_db[i].duration_traffic, 
                        'End_Address' : data_db[i].end_address, 'Start_Address' : data_db[i].start_address,
                        'Speed_Without_Traffic' : data_db[i].speed_no_traffic,
                        'Speed_With_Traffic' : data_db[i].speed_w_traffic, 'Time' : data_db[i].t_human,
                        'Route' : data_db[i].route } 
                for i in range(len(data_db))}
        traffic_data = {'traffic_data' : data}
        del (data)
        end_time = time.time()
        print("time taken ", end_time - start_time)
        return jsonify(traffic_data)


    
@api.route('/v2/traffic/end/', methods = ['GET'])
def traffic_endStations():
    #END ADDRESS LIST AND EXISTS
    try:
        if request.args.get('city'):
            city = request.args.get('city')
        else: 
            city = "Delhi"
            
    except ValueError as valueerr:
        print("ValueError has been raised." )
        print(valueerr)
    except TypeError as typeerr:
        print("Type error has been raised.")
        print(typeerr)
        
    if city == "Delhi":
        conn = DelhiTraffic
    elif city == "Banglore":
        conn = BangloreTraffic
    elif city == "Mumbai":
        conn = MumbaiTraffic
    else:
        conn = DelhiTraffic
    
    Validation.city_validation(conn, city)
    
    data_db = conn.query.distinct(conn.end_address).group_by(conn.end_address)
    print(type(data_db))
    print(data_db.count())
    #print(len(data_db))
    if(data_db.count() == 0):
        raise NotFoundError({'city' : city}, message = 'This city doesn\'t match any record')
    else:
        start_time = time.time()
        data = { i+1 : data_db[i].end_address for i in range(data_db.count())}
        traffic_data = {'start_stations' : data}
        print(traffic_data)
        del (data)
        end_time = time.time()
        print("time taken ", end_time - start_time)
        return jsonify(traffic_data)
    

    
@api.route('/v2/traffic/start/', methods = ['GET'])
def traffic_startStations():
    #START ADDRESS LIST AND EXISTS
    try:
        if request.args.get('city'):
            city = request.args.get('city')
        else: 
            city = "Delhi"
            
    except ValueError as valueerr:
        print("ValueError has been raised." )
        print(valueerr)
    except TypeError as typeerr:
        print("Type error has been raised.")
        print(typeerr)
        
    if city == "Delhi":
        conn = DelhiTraffic
    elif city == "Banglore":
        conn = BangloreTraffic
    elif city == "Mumbai":
        conn = MumbaiTraffic
    else:
        conn = DelhiTraffic
    
    Validation.city_validation(conn, city)
    
    data_db = conn.query.distinct(conn.start_address).group_by(conn.start_address)
    print(type(data_db))
    print(data_db.count())
    #print(len(data_db))
    if(data_db.count() == 0):
        raise NotFoundError({'city' : city}, message = 'This city doesn\'t match any record')
    else:
        start_time = time.time()
        data = { i+1 : data_db[i].start_address for i in range(data_db.count())}
        traffic_data = {'start_stations' : data}
        print(traffic_data)
        del (data)
        end_time = time.time()
        print("time taken ", end_time - start_time)
        return jsonify(traffic_data)
    
@api.route('/v2/traffic/add/', methods = ['POST'])
def traffic_add():
    if not request.json or not 'date_time' in request.json or not 'city' in request.json:
        abort (400)
    if request.args.get('date_time'):
        date_time = request.json['date_time']
        city = request.json['city']
        distance = request.json['distance']
        duration = request.json['duration']
        duration_traffic = request.json['duration_traffic']
        end_address = request.json['end_address']
        start_address = request.json['start_address']
        speed_no_traffic = request.json['speed_no_traffic']
        speed_w_traffic = request.json['speed_w_traffic']        
        #timestamp and human time stamp is remaining 


@api.route('/v1/<string:City>/<string:from_station>/<string:to_station>/<string:date_time>/', methods = ['GET'])
def traffic1(City, from_station, to_station, date_time):
    
    if City == "Delhi":
        conn = DelhiTraffic
    elif City == "Banglore":
        conn = BangloreTraffic
    elif City == "Mumbai":
        conn = MumbaiTraffic
    else :
        conn = DelhiTraffic
    
    
    print(type(date_time))
    print(date_time)
    data_db = conn.query.filter(conn.start_address.like('%'+from_station+'%'), 
                                conn.end_address.like('%'+to_station+'%'), conn.t == date_time).all()
    print(len(data_db))
    
    print(len(data_db))
    print((data_db[0]))
    data = {}
    for i in range(len(data_db)):
        print(i)
        data[i + 1] = {'Distance': data_db[i].distance, 'Duration' : data_db[i].duration, 
                        'Duration_Traffic' : data_db[i].duration_traffic, 'End_Address' : data_db[i].end_address, 
                        'Start_Address' : data_db[i].start_address, 'Speed_Without_Traffic' : data_db[i].speed_no_traffic, 
                        'Speed_With_Traffic' : data_db[i].speed_w_traffic, 'Time' : data_db[i].t_human,  
                        'Route' : data_db[i].route}
        print(data_db[i])
    traffic_data = {'traffic_data' : data}
    del (data)
    return jsonify(traffic_data)


#@api.errorhandler(400)
@api.errorhandler(ValidationError)
def handle_ValidationError(error):
    response = jsonify(error.to_dict())
    return response

@api.errorhandler(404)
def NotFoundDefault(error):
    print(error)
    #response = jsonify(error.to_dict())
    return error

@api.errorhandler(NotFoundError)
def handle_NotFoundError(error):
    print(error)
    response = jsonify(error.to_dict())
    return response

@api.errorhandler
def default_error_handler(error):
    error = ServerError()
    return error.to_dict(), getattr(error, 'code', 500)

if __name__ == '__main__':
    db.init_app(api)
    api.run(debug = True)
    
#http://127.0.0.1:5000/v1/traffic/?city=Delhi&date_time=201706130430&from_station=MSIL%20Internal%20Rd,%20Maruti%20Udyog,%20Sector%2018,%20Gurugram,%20Haryana%20122008,%20India&to_station=%27Civil%20Lines,%20Gurugram,%20Haryana%20122022,%20India%27
#http://127.0.0.1:5000/v1/Delhi/West%20Delhi,%20New%20Delhi,%20Delhi%20110009,%20India/Outer%20Ring%20Rd,%20Delhi,%20India/201704051500/
#http://127.0.0.1:5000/v2/traffic/?city=Mumbai&date_time=201706130430&start_station=Teen Murti Marg, Teen Murti Bhavan, New Delhi, Delhi 110011, India&end_station=Terminal 1D Departure Rd, Indira Gandhi International Airport, New Delhi, Delhi, India