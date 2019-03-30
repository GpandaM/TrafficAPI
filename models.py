# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:52:20 2018

@author: garima.misra
"""


#from app import db
import numpy as np
from datetime import datetime

from flask import Flask, jsonify, render_template, abort, request, make_response
from flask_sqlalchemy import SQLAlchemy


from marshmallow import Schema, fields, validates_schema, ValidationError, validates

api = Flask(__name__)
api.config.from_pyfile('Config.py')
#api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(api)

class DelhiTraffic(db.Model):
    __tablename__ = 'traffic'
    distance = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    duration_traffic = db.Column(db.Integer)
    end_address = db.Column(db.String(50))
    start_address = db.Column(db.String(50))
    t = db.Column(db.Integer, primary_key = True)
    speed_no_traffic = db.Column(db.Float)
    speed_w_traffic = db.Column(db.Float)
    t_human = db.Column(db.DateTime, primary_key = True)
    route = db.Column(db.String(50))
    
    def __init__(self, distance, duration, traffic_duration, from_address,
                 to_address, timestamp, speed_no_traffic, speed_w_traffic, date_time, route):
        self.distance = distance
        self.duration = duration
        self.duration_traffic = traffic_duration
        self.end_address  = to_address
        self.start_address = from_address
        self.t = timestamp
        self.speed_no_traffic = speed_no_traffic
        self.speed_w_traffic = speed_w_traffic
        self.t_human = date_time
        self.route = route
        self.created_at = datetime.datetime.now()
        
    def __repr__(self):
        return '<%s, %s, %s, %s, %s, %s, %s, %s, %s, %s>' %(self.distance, self.duration, self.duration_traffic,
                                                            self.end_address, self.start_address, self.t, self.speed_no_traffic,
                                                            self.speed_w_traffic, self.t_human, self.route)


class MumbaiTraffic(DelhiTraffic):
    __bind_key__  = 'Mumbai'
    __tablename__ = 'traffic'
    
class BangloreTraffic(DelhiTraffic):
    __bind_key__ = 'Banglore'
    __tablename__ = 'traffic'
    

class DelhiTrafficSchema(Schema):
    distance = fields.Integer()
    duration = fields.Integer()
    duration_traffic = fields.Integer()
    end_address = fields.String(required = True)
    start_address = fields.String(required = True)
    t = fields.Integer()
    speed_no_traffic = fields.Float()
    speed_w_traffic = fields.Float()
    t_human = fields.DateTime(required = True)
    route = fields.String()
    created_at = fields.DateTime()
    
    @validates_schema
    def validate_addresss(self, data):
        if data['end_address'] == data['start_address']:
            raise ValidationError("Start address and end address can not be same", {'status_code' : 422})
            
    @validates('distance')
    def validate_distance(self, value):
        if value == 0:
            raise ValidationError("Distance can not be Zero", {'status_code' : 422})
            
    @validates('duration')
    def validate_duration(self, value):
        if value == 0:
            raise ValidationError("Duration can not be zero", {'status_code' : 422})
    