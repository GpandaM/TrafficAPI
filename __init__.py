# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 16:46:54 2018

@author: garima.misra
"""
from flask import Flask 

from models import DelhiTraffic, MumbaiTraffic, BangloreTraffic
#from app import 

api = Flask(__name__)