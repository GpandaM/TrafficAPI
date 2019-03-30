# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 22:47:32 2018

@author: garima.misra
"""
from flask import Flask

class BaseError(Exception):
    def __init__(self, code = 400, message = '', status = '', field = None):
        Exception.__init__(self)
        self.code = code
        self.message = message
        self.status = status
        self.field = field
        
    def to_dict(self):
        return {'code' : self.code, 'message' : self.message, 'status' : self.status, 'field' : self.field, }
    
class ValidationError(BaseError):
    def __init__(self, field, message = 'Invalid Field'):
        BaseError.__init__(self)
        self.code = 400
        self.message = message
        self.status = 'INVALID_FIELD'
        self.field = field
        
class NotFoundError(BaseError):
    def __init__(self, field, message = 'Not Found'):
        BaseError.__init__(self)
        self.code = 404
        self.message = message
        self.status = 'NOT_FOUND'
        self.field = field

class ServerError(BaseError):
    def __init__(self, message = 'Internal Server Error'):
        BaseError.__init__(self)
        self.code = 500
        self.message = message
        self.status = 'SERVER_ERROR'
        

class Validation:
    def __init__(self):
        pass
#    def __init__(self, conn, date_time, city, start_station, end_station):
#        self.conn = conn
#        self.date_time = date_time
#        self.city = city
#        self.start_station = start_station
#        self.end_station = end_station
    
    
    @staticmethod
    def date_time_validation(conn, date_time):
        #DATE TIME VALIDATION
        if(len(date_time) != 12):
            raise ValidationError('date_time' , message = 'date_time has not been entered correctly')
        elif ( (conn.query.filter_by(t = date_time).count()) == 0 ):
            raise ValidationError('date_time' , message = 'This date_time doesn\'t exists in database')
        else :
            print("DATE TIME VALIDATION IS POSITIVE")
        
   
    @staticmethod
    def city_validation(conn, city):
        #CITY VALIDATION
        city_list = ['Delhi', 'Banglore', 'Mumbai']
        if city not in city_list:
            raise ValidationError('city', message = 'City doesn\'t exists in database')
        else:
            print("CITY VALIDATION IS POSITIVE")
        
    
    @staticmethod
    def start_station_validation(conn, start_station):
        #START STATION VALIDATION
        if((conn.query.filter(conn.start_address.like('%'+start_station+'%'))).count() == 0):
            raise ValidationError('start_station', message = 'start_station doesn\'t exists in database')
        else:
            print("START_STATION IS POSITIVE")
        
   
    @staticmethod
    def end_station_validation(conn, end_station):
        #END STATION VALIDATION
        if((conn.query.filter(conn.end_address.like('%'+end_station+'%'))).count() == 0):
            raise ValidationError('end_station', message = 'end_station doesn\'t exists in database')
        else:
            print("END_STATION IS POSITIVE")