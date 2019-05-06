# Database models
from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from flask import jsonify, Flask
import json
import datetime

from api.db import Base

class Measurements(Base):
    __tablename__ = 'Measurements'
    id = Column(Integer, primary_key=True)
    s_time = Column(TIMESTAMP, unique=True)
    e_time = Column(TIMESTAMP, unique=True)
    data = Column(JSON, unique=True)

    def __init__(self, id=None, s_time=None, e_time=None, data=None):
        self.id = id
        self.s_time = s_time
        self.e_time = e_time
        self.data = data

    # from object to JSON
    def jsonize(self):
        return {'id': self.id,
                's_time': self.s_time.timestamp(),
                'e_time': self.e_time.timestamp(),
                'data': self.data }
