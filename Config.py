# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:50:39 2018

@author: garima.misra
"""

import os

basedir = os.path.abspath(os.path.dirname(os.getcwd()))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'traffic.db')
SQLALCHEMY_BINDS = {
        'Mumbai' : 'sqlite:///' + os.path.join(basedir, 'traffic_Mumbai.db'),
        'Banglore' : 'sqlite:///' + os.path.join(basedir, 'traffic_Banglore.db')
        }
#SQLALCHEMY_TRACK_MODIFICATIONS  = False

print(SQLALCHEMY_DATABASE_URI)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


