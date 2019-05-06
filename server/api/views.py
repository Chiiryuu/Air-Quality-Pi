# all API routes
from sqlalchemy import between
from sqlalchemy.sql import select
from flask import Flask, request, jsonify, session, send_file
import datetime
import base64
import json
import os

from api import app
import api.db
from api.db import db_session
from api.db import init_db
from api.models import Measurements
from api.config import BaseConfig

app.config.from_object(BaseConfig)
init_db()

# Endpoint for uploading test data
@app.route('/upload', methods=['POST'])
def upload():
    json_data = request.json
    print("/upload", json_data, "\n")
    mesurement = Measurements(s_time = datetime.datetime.fromtimestamp(json_data['s_time']/1e3),
            e_time = datetime.datetime.fromtimestamp(json_data['e_time']/1e3),
            data = json_data['data']) # Constructs a new mesurement object

    try:
        db_session.add(mesurement) # adds new mesurement object to the database
        db_session.commit()
        status = 'success'
    except Exception as e:
        print("Error occured trying to upload data:", e)
        status = 'failure'
    finally:
        db_session.close()

    return jsonify({'result': status})

# Endpoint for querying the database data
@app.route('/data', methods=['GET'])
def get_data():
    json_data = request.json
    print("/data", json_data, "\n")

    q_stime = datetime.datetime.fromtimestamp(json_data['s_time']/1e3) # conversions from database date string to timestamp number
    q_etime = datetime.datetime.fromtimestamp(json_data['e_time']/1e3)

    try:
        statement = select([Measurements]).where(between(Measurements.s_time, q_stime, q_etime) | between(Measurements.e_time, q_stime, q_etime)) # select statement on the database
        results = db_session.execute(statement).fetchall()
        print(results)
        result = []
        for row in results: # formats the results into a JSON list
            tmp = Measurements(id=row['id'], s_time=row['s_time'], e_time=row['e_time'], data=row['data'])
            result.append(tmp.jsonize())

    except Exception as e:
        print("Error occured trying to upload data:", e)
        result = {'result': 'failure'}
    finally:
        db_session.close()

    return jsonify(result)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
